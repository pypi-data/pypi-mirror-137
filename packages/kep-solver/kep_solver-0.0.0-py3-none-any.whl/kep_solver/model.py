from collections.abc import ValuesView
from enum import Enum

import pulp  # type: ignore

from kep_solver.entities import Instance, Donor
from kep_solver.graph import CompatibilityGraph, Vertex


class Sense(Enum):
    """An enumeration of the sense of an objective."""

    MAX = 1
    MIN = 2
    EXACT = 3

    def toConstraint(self):
        """Converts a Sense into a constraint type suitable for use
        with PuLP

        :return: constraint sense
        """
        if self.name == "MAX":
            return pulp.LpConstraintGE
        elif self.name == "MIN":
            return pulp.LpConstraintLE
        else:
            return pulp.LpConstraintEQ

    def toObjective(self):
        """Converts a Sense into an objective type suitable for use
        with PuLP

        :return: objective sense
        """
        if self.name == "MAX":
            return pulp.LpMaximize
        elif self.name == "MIN":
            return pulp.LpMinimize
        else:
            raise Exception("Exact objective doesn't make sense")


class Objective:
    """A base class for an objective."""

    def __init__(self):
        raise Exception("Plain Objective objects cannot be instantiated")

    def value(self, graph: CompatibilityGraph, exchange: list[Vertex]) -> float:
        """What value should the given exchange in the given graph
        be given?

        :param graph: The graph containing the exchange
        :param exchange: A cycle or chain.
        """
        pass

    def describe(self) -> str:
        """Describes what this objective optimises.

        :return: the description
        """
        raise Exception("Plain Objective objects cannot be instantiated")

    @property
    def sense(self) -> Sense:
        """The sense of the objective."""
        pass


class TransplantCount(Objective):
    """An objective to maximise the number of transplants. Note that
    for a chain, the donation to the non-directed donor (which often
    would go to a deceased-donor waiting list) is counted as a
    transplant.
    """

    def __init__(self):
        pass

    def value(self, graph: CompatibilityGraph, exchange: list[Vertex]) -> float:
        """How many transplants does the given exchange represent.

        :param graph: The graph containing the exchange
        :param exchange: A cycle or chain.
        :return: the number of transplants
        """
        return len(exchange)

    def describe(self) -> str:
        """Describes what this objective optimises.

        :return: the description
        """
        return "Number of transplants"

    @property
    def sense(self) -> Sense:
        """This is a maximisation objective."""
        return Sense.MAX


class EffectiveTwoWay(Objective):
    """An objective to maximise the number of effective two-way
    transplants.  For cycles, they must either have size two, or have
    a back-arc. All chains count as effective two-way exchanges. This
    is binary for each exchange.  That is, either an exchange has or
    does not have an effective two-way exchange.
    """

    def __init__(self):
        pass

    def value(self, graph: CompatibilityGraph, exchange: list[Vertex]) -> float:
        """Does the given exchange contain an effective two-way
        exchange?

        :param graph: The graph containing the exchange
        :param exchange: A cycle or chain.
        :return: 1 if and only if it is effectively two-way
        """
        if exchange[0].isNdd():
            return 0
        if len(exchange) == 2:
            return 1
        if len(exchange) == 3 and graph.numBackArcs(exchange) >= 1:
            return 1
        return 0

    def describe(self) -> str:
        """Describes what this objective optimises.

        :return: the description
        """
        return "Number of effective two-way exchanges"

    @property
    def sense(self) -> Sense:
        """This is a maximisation objective."""
        return Sense.MAX


class BackArcs(Objective):
    """An objective to maximise the number of back-arcs. Note that
    arcs back to a non-directed donor are not considered backarcs in
    this objective.
    """

    def __init__(self):
        pass

    def value(self, graph: CompatibilityGraph, exchange: list[Vertex]) -> float:
        """How many backarcs does the given exchange contain?

        :param graph: The graph containing the exchange
        :param exchange: An exchange
        :return: The number of backarcs in the exchange
        """
        if len(exchange) == 3:
            if exchange[0].isNdd():
                return 1 + graph.numBackArcs(exchange)
            return graph.numBackArcs(exchange)
        return 0

    def describe(self) -> str:
        """Describes what this objective optimises.

        :return: the description
        """
        return "Number of backarcs"

    @property
    def sense(self) -> Sense:
        """This is a maximisation objective."""
        return Sense.MAX


class UKScore(Objective):
    """An objective to maximise the number of back-arcs."""

    _age_weight_selector = 20
    _age_weight = 3
    _age_diff_factor = 1e-5
    _max_age_diff = 70

    def __init__(self):
        pass

    def value(self, graph: CompatibilityGraph, exchange: list[Vertex]) -> float:
        """What is the score (UK) of this exchange?

        :param graph: The graph containing the exchange
        :param exchange: An exchange
        :return: The number of backarcs in the exchange
        """
        score: float = 0.0
        for ind, source in enumerate(exchange):
            target_v = exchange[(ind + 1) % len(exchange)]
            donor = source.donor
            if not target_v.donor.NDD:
                recipient = target_v.donor.recipient
                transplants = [
                    t for t in donor.transplants() if t.recipient == recipient
                ]
                assert len(transplants) == 1
                transplant = transplants[0]
                score += transplant.weight
                age_diff = abs(donor.age - target_v.donor.age)
                if age_diff <= self._age_weight_selector:
                    score += self._age_weight
                age_diff_score = (self._max_age_diff - age_diff) ** 2
                score += self._age_diff_factor * age_diff_score
        return score

    def describe(self) -> str:
        """Describes what this objective optimises.

        :return: the description
        """
        return "Total score"

    @property
    def sense(self) -> Sense:
        """This is a maximisation objective."""
        return Sense.MAX


class ThreeWay(Objective):
    """An objective to minimise the number of three-way exchanges. If
    no larger exchanges are allowed, this has the effect of increasing
    the number of two-way exchanges.
    """

    def __init__(self):
        pass

    def value(self, graph: CompatibilityGraph, exchange: list[Vertex]) -> float:
        """Is the given exchange a three-way exchange.

        :param graph: The graph containing the exchange
        :param exchange: A cycle or chain.
        :return: 1 if and only if it is a three-way exchange
        """
        if len(exchange) == 3:
            return 1
        return 0

    def describe(self) -> str:
        """Describes what this objective optimises.

        :return: the description
        """
        return "Number of three-way exchanges"

    @property
    def sense(self) -> Sense:
        """This is a minimisation objective."""
        return Sense.MIN


class Model(pulp.LpProblem):
    """A base class for all models for KEPs. Any new models should
    inherit from this and implement all associated functions.
    """

    supports: list[type[Objective]] = []

    def __init__(self):
        super().__init__()

    def support(self, objective: Objective) -> bool:
        """Can this model solve for the given objective.

        :param objective: The objective to solve
        :return: Can this model solve the given objective
        """
        return bool([isinstance(objective, supported) for supported in self.supports])

    def addObjectiveConstraint(self, objective: Objective, value: float, index: int):
        """Add a constraint that ensures the previous objective keeps
        its value.

        :param objective: The previous objective
        :param value: The value the previous objective attained
        :param index: Which number objective is this (only used for
        naming the constraint)
        """
        pass

    def solve(self) -> list[list[Vertex]]:
        """Solve the model to find an optimal solution.

        :return: A list of selected transplants
        """
        pass


class CycleAndChainModel(Model):
    """A model that represents each cycle or chain with a binary
    variable.  Note that since CompatibilityGraph has one vertex per
    donor, and recipients may have multiple donors, this means that
    constraints may be needed to ensure at most one donor per recipient
    is selected.

    """

    supports = [TransplantCount]

    def __init__(
        self,
        instance: Instance,
        objectives: list[Objective],
        *,
        maxCycleLength: int,
        maxChainLength: int,
    ):
        super().__init__()
        self._instance: Instance = instance
        self._graph: CompatibilityGraph = CompatibilityGraph(instance)
        # List comprehension to make a copy of the list of objectives
        self._objectives: list[Objective] = [obj for obj in objectives]
        self._maxCycleLength = maxCycleLength
        self._maxChainLength = maxChainLength
        self._cycles: dict[pulp.LpVariable, list[Vertex]] = {}
        self._chains: dict[pulp.LpVariable, list[Vertex]] = {}
        self._objective_values: list[float] = []
        self._vars_by_vertex: dict[Vertex, list[pulp.LpVariable]] = {}
        self._vars_by_exchange: dict[tuple[Vertex, ...], pulp.LpVariable] = {}

    @property
    def cycles(self) -> ValuesView[list[Vertex]]:
        """Return the list of cycles in this model.

        :return: the list of cycles
        """
        return self._cycles.values()

    @property
    def chains(self) -> ValuesView[list[Vertex]]:
        """Return the list of chains in this model.

        :return: the list of chains
        """
        return self._chains.values()

    @property
    def exchanges(self) -> list[list[Vertex]]:
        """Return the list of chains in this model.

        :return: the list of chains
        """
        return list(self.chains) + list(self.cycles)

    def exchange_values(self, exchange: list[Vertex]) -> list[float]:
        """Given an exchange, return the value of the exchange for
        each objective.

        :param exchange: The exchange whose value is to be returned
        :return: the list of values of this exchange
        """
        return [
            objective.value(self._graph, exchange) for objective in self._objectives
        ]

    def _var_from_donor(self, donor: Donor) -> pulp.LpVariable:
        """Given a donor, find its corresponding variable. This means
        going via the CompatibilityGraph.

        :param donor: the donor to search for
        :return: the donor's variable
        """
        return self._vars_by_vertex[self._graph.donorVertex(donor)]

    def _var_from_exchange(self, exchange: list[Vertex]) -> pulp.LpVariable:
        """Given an exchange, get the variable representing it.

        :param exchange: the exchange to search for
        :return: the exchange's variable
        """
        # Turn list to tuple for dict access
        key = tuple(exchange)
        return self._vars_by_exchange[key]

    def build_model(self):
        """Build the model. That is, create all the variables and
        constraints."""
        # Track the chains each NDD can be in
        chains_by_ndd: dict[Donor, list[pulp.LpVariable]] = {}
        for nondirected in self._instance.donors():
            if not nondirected.NDD:
                continue
            chains_by_ndd[nondirected] = []
        for vertex in self._graph.vertices:
            self._vars_by_vertex[vertex] = []
        for cycle in self._graph.findCycles(self._maxCycleLength):
            var = pulp.LpVariable(f"cycle_{len(self._cycles)}", cat="Binary")
            for vertex in cycle:
                self._vars_by_vertex[vertex].append(var)
            self._vars_by_exchange[tuple(cycle)] = var
            self._cycles[var] = cycle
        for chain in self._graph.findChains(self._maxChainLength):
            var = pulp.LpVariable(f"chain_{len(self._chains)}", cat="Binary")
            for vertex in chain:
                self._vars_by_vertex[vertex].append(var)
            self._chains[var] = chain
            chains_by_ndd[chain[0].donor].append(var)
            self._vars_by_exchange[tuple(chain)] = var
        for recipient in self._instance.recipients():
            name = f"recipient_{str(recipient)}"
            self += (
                pulp.lpSum(self._var_from_donor(donor) for donor in recipient.donors())
                <= 1,
                name,
            )
        # Add constraint that each NDD can be used at most once.
        for nondirected in self._instance.donors():
            if not nondirected.NDD:
                continue
            name = f"ndd_{str(nondirected)}"
            self += pulp.lpSum(chains_by_ndd[nondirected]) <= 1, name

    def addObjectiveConstraint(self, objective: Objective, value: float, index: int):
        """Adds a constraint that ensures the previous objective keeps
        its value.

        :param objective: The previous objective
        :param value: The value the previous objective attained
        :param index: Which number objective is this (only used for
            naming the constraint)
        """
        equation = pulp.lpSum(
            objective.value(self._graph, cycle) * var
            for var, cycle in self._cycles.items()
        )
        equation += pulp.lpSum(
            objective.value(self._graph, chain) * var
            for var, chain in self._chains.items()
        )
        con = pulp.LpConstraint(
            equation,
            sense=objective.sense.toConstraint(),
            rhs=value,
            name=f"ObjCon_{index}",
        )
        self += con

    def solve(self) -> list[list[Vertex]]:
        """Solve the model to find an optimal solution.

        :return: A list of selected transplants
        """
        self.build_model()
        selected: list[list[Vertex]] = []
        for index, obj in enumerate(self._objectives):
            exchanges: list[list[Vertex]] = list(self._cycles.values())
            exchanges += list(self._chains.values())
            obj_equation = pulp.lpSum(
                obj.value(self._graph, exchange) * self._var_from_exchange(exchange)
                for exchange in exchanges
            )
            self += obj_equation
            self.sense = obj.sense.toObjective()
            solver = pulp.getSolver("PULP_CBC_CMD", msg=False)
            pulp.LpProblem.solve(self, solver)
            self._objective_values.append(pulp.valueOrDefault(self.objective))
            if index < len(self._objectives) - 1:
                self.addObjectiveConstraint(obj, self._objective_values[-1], index)
            else:
                for var, cycle in self._cycles.items():
                    if var.value() > 0.9:
                        selected.append(cycle)
                for var, chain in self._chains.items():
                    if var.value() > 0.9:
                        selected.append(chain)
        return selected

    @property
    def objective_values(self) -> list[float]:
        """The list of all objective values."""
        return self._objective_values

    def objective_value(self, objective_index: int) -> float:
        """Return the value of an objective, if it has been solved.
        If this model has not been solved, accessing this raises an
        error.

        :param objective_index: the index of the objective whose value
            is to be returned
        :return: the value of the objective as given by objective_index
        """
        if not self._objective_values:
            raise Exception(
                "Tried to get objective value when model is not solved."
            )
        return self._objective_values[objective_index]
