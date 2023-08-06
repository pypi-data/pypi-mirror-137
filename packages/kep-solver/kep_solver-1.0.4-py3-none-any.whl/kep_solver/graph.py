"""Describes a number of classes related to the compatibility graph."""
from __future__ import annotations
from typing import Any, Union, Optional

from kep_solver.entities import Donor, Recipient


class Vertex:
    """A vertex in a digraph representing a donor (directed or
    non-directed)."""

    def __init__(self, index: int, represents: Donor) -> None:
        self._index: int = index
        self._represents: Donor = represents
        self._properties: dict[str, Any] = {}
        self._edges_out: list[Edge] = []
        self._edges_in: list[Edge] = []

    @property
    def index(self) -> int:
        """Get the index (in the graph) of this vertex.

        :return: the index
        """
        return self._index

    def isNdd(self) -> bool:
        """Return True if this vertex corresponds to a non-directed
        donor.

        :return: True if this vertex corresponds to a non-directed
            donor
        """
        return self.donor.NDD

    @property
    def donor(self) -> Donor:
        """Return the donor associated with this vertex.

        :return: the associated donor"""
        return self._represents

    def addEdgeIn(self, edge: Edge) -> None:
        """Add an edge leading in to this vertex.

        :param edge: the edge
        """
        self._edges_in.append(edge)

    def addEdgeOut(self, edge: Edge) -> None:
        """Add an edge leading out from this vertex.

        :param edge: the edge
        """
        self._edges_out.append(edge)

    @property
    def edgesIn(self) -> list[Edge]:
        """Return the list of edges leading in to this vertex.

        :return: the list of edges leading in to this vertex.
        """
        return self._edges_in

    @property
    def edgesOut(self) -> list[Edge]:
        """Return the list of edges leading out from this vertex.

        :return: the list of edges leading out of this vertex.
        """
        return self._edges_out

    def adjacent(self) -> list[Vertex]:
        """Return the neighbours of this vertex

        :return: the list of neighbouring vertices
        """
        return [edge.end for edge in self.edgesOut]

    def __str__(self) -> str:
        """Return a string representation of the vertex."""
        if self.isNdd():
            return f"V({self.donor} ({self.index}))"
        else:
            return f"V({self.donor},{self.donor.recipient} ({self.index}))"

    def __repr__(self) -> str:
        return str(self)


class Edge:
    """An edge in a digraph, representing a potential transplant. An
    edge is always associated with a donor.
    """

    def __init__(self, donor: Donor, start: Vertex, end: Vertex) -> None:
        self._donor: Donor = donor
        self._properties: dict[str, Any] = {}
        self._start_vertex: Vertex = start
        self._end_vertex: Vertex = end

    @property
    def donor(self) -> Donor:
        """Return the donor associated with this transplant.

        :return: The associated donor
        """
        return self._donor

    @property
    def end(self) -> Vertex:
        """Return the end-point of this edge.

        :return: the end Vertex of this edge
        """
        return self._end_vertex

    def addProperty(self, name: str, value) -> None:
        """Add an arbitrary property to this edge. This can be used
        for e.g. a score value associated with the transplant.

        :param name: the name of the property
        """
        self._properties[name] = value

    def getProperty(self, name: str) -> Any:
        """Get a property of this transplant.

        :param name: the name of the property
        :return: the associated value, which may have any type
        """
        return self._properties[name]


class CompatibilityGraph:
    """A digraph representing a KEP instance. Note that each vertex is
    a donor. Each edge corresponds to a potential transplant, and thus
    is associated with a donor that is paired with the recipient at
    beginning of the arc.
    """

    def __init__(self, instance=None):
        self._vertices: list[Vertex] = []
        self._edges: list[Edge] = []

        # Map each recipient or ndd to a vertex object
        self._vertex_map: dict[Union[Donor, Recipient], Vertex] = {}
        if instance is not None:
            for donor in instance.donors():
                self.addDonor(donor)
            for transplant in instance.transplants():
                self.addEdges(
                    transplant.donor,
                    transplant.recipient,
                    properties={"weight": transplant.weight},
                )

    @property
    def size(self) -> int:
        """The number of vertices in the graph.

        :return: the number of vertices
        """
        return len(self._vertices)

    @property
    def vertices(self) -> list[Vertex]:
        """The vertices in the graph.

        :return: the vertices
        """
        return self._vertices

    def edges(self) -> list[Edge]:
        """The edges in the graph.

        :return: the edges
        """
        return self._edges

    def addDonor(self, donor: Donor) -> None:
        """Add a vertex representing a donor.

        :param donor: a donor to be added to the graph.
        """
        vertex = Vertex(len(self._vertices), donor)
        self._vertices.append(vertex)
        self._vertex_map[donor] = vertex

    def donorVertex(self, donor: Donor) -> Vertex:
        """Get the vertex associated with a donor.

        :param donor: the donor to find
        :return: the vertex associated with the donor
        """
        return self._vertex_map[donor]

    def addEdges(self, donor: Donor, recip: Recipient, **properties: dict[str, Any]):
        """Add edges to the digraph corresponding to some potential
        transplant, optionally with some additional properties. Note
        that since the graph uses donors to represent vertices, if the
        given recipient has multiple donors then one edge will be added
        for each paired donor

        :param donor: the donor in the transplant
        :param recip: the recipient in the transplant
        :param properties: an optional dictionary mapping property
            names (as strings) to properties
        """
        start = self._vertex_map[donor]
        for pairedDonor in recip.donors():
            end = self._vertex_map[pairedDonor]
            edge = Edge(donor, start, end)
            for name, value in properties.items():
                edge.addProperty(name, value)
            start.addEdgeOut(edge)
            end.addEdgeIn(edge)
            self._edges.append(edge)

    def embeddedExchanges(self, exchange: list[Vertex]) -> list[list[Vertex]]:
        """Determines the embedded exchanges in the given exchange.
        Note that this only functions for exchanges of size at most
        three.

        :param exchange: The exchange (either as a cycle or a chain) in
            question. This must contain at most three vertices.
        :return: a list containing one list[Vertex] for each embedded
            exchange
        """
        ret: list[list[Vertex]] = []
        if len(exchange) == 2:
            return ret
        assert len(exchange) == 3
        if exchange[0] in exchange[1].adjacent():
            ret.append([exchange[0], exchange[1]])
        if exchange[1] in exchange[2].adjacent():
            ret.append([exchange[1], exchange[2]])
        if exchange[2] in exchange[0].adjacent():
            ret.append([exchange[0], exchange[2]])
        return ret

    def numBackArcs(self, exchange: list[Vertex]) -> int:
        """Determines the number of back-arcs in the given exchange.
        Note that backarcs are only defined for exchanges with size
        three.

        :param exchange: The exchange (either as a cycle or a chain) in
            question. This must contain exactly three vertices.
        :return: the number of back-arcs
        """
        assert len(exchange) == 3
        num = 0
        if exchange[0] in exchange[1].adjacent():
            num += 1
        if exchange[1] in exchange[2].adjacent():
            num += 1
        if exchange[2] in exchange[0].adjacent():
            num += 1
        return num

    def findChains(self, maxChainLength: int) -> list[list[Vertex]]:
        """Finds and returns all chains in this graph. Note that this
        is specifically chains, and does not include cycles.

        :param maxchainLength: the maximum length of any chain
        :returns: a list of chains, where each chain is represented as
            a list of vertices
        """
        chains: list[list[Vertex]] = []
        used = [False] * self.size
        stack: list[Vertex] = []

        def _extend(v: Vertex):
            chains.append([vert for vert in stack])
            if len(stack) == maxChainLength:
                return
            for w in v.adjacent():
                if not used[w.index]:
                    used[w.index] = True
                    stack.append(w)
                    _extend(w)
                    stack.pop()
                    used[w.index] = False

        for vert in self.vertices:
            if not vert.isNdd():
                continue
            used = [False] * self.size
            stack = [vert]
            _extend(vert)
        return chains

    def findCycles(self, maxCycleLength: int) -> list[list[Vertex]]:
        """Finds and returns all cycles in this graph. Note that this
        is specifically cycles, and does not include chains.

        :param maxCycleLength: the maximum length of any cycle
        :returns: a list of cycles, where each cycle is represented as
        a list of vertices
        """
        # Implementing a variant of Johnson's algorithm from
        # Finding All The Elementary Circuits of a Directed Graph,
        # Donald B. Johnson, SIAM J.
        # Comput., 1975
        # There are some changes, however. Blocklists (B(n) in the
        # paper) aren't used, as since we limit cycle lengths we will
        # return when the stack is too long, but that doesn't mean we
        # must've created all cycles through a given vertex. For the
        # same reason, v is unblocked after each visit, regardless of
        # whether we find any cycles
        blocked: list[bool] = [False] * self.size
        stack: list[int] = []
        cycles: list[list[int]] = []

        def _unblock(u: int):
            blocked[u] = False

        def _circuit(v: int, component: list[int]) -> bool:
            flag = False
            if len(stack) == maxCycleLength:
                return False
            stack.append(v)
            blocked[v] = True
            for w in self.vertices[v].adjacent():
                if w.index not in component:
                    continue
                if w.index == s:
                    flag = True
                    cycles.append(list(stack + [s]))
                elif not blocked[w.index]:
                    if _circuit(w.index, component):
                        flag = True
            _unblock(v)
            stack.pop(-1)
            return flag

        s = 0

        def _tarjan(num_forbidden_vertices: int) -> Optional[list[int]]:
            index = 0
            component = None
            stack = list()
            indices = [-1] * self.size
            lowlink = [-1] * self.size
            onStack = [False] * self.size

            def _strongconnect(v: int, index: int) -> tuple[int, Optional[list[int]]]:
                indices[v] = index
                lowlink[v] = index
                index += 1
                onStack[v] = True
                component = None
                stack.append(v)
                for w in self.vertices[v].adjacent():
                    if w.index < num_forbidden_vertices:
                        continue
                    if indices[w.index] == -1:
                        index, component = _strongconnect(w.index, index)
                        lowlink[v] = min(lowlink[v], lowlink[w.index])
                    elif onStack[w.index]:
                        lowlink[v] = min(lowlink[v], indices[w.index])
                if lowlink[v] == indices[v]:
                    component = stack
                return index, component

            for v in range(num_forbidden_vertices, self.size):
                if indices[v] == -1:
                    index, component = _strongconnect(v, index)
                if component is not None:
                    return component
            return None

        while s < self.size:
            # Let Ak be adj matrix of strongly connected component K of
            # the induced graph on {s, s+1, ... , n} that contains the
            # lowest vertex
            component = _tarjan(s)
            if component is None:
                s = self.size
            else:
                s = component[0]
                for i in component:
                    blocked[i] = False
                _circuit(s, component)
                s += 1

        realCycles: list[list[Vertex]] = []
        for indices in cycles:
            # Johnson's always adds the first vertex onto the end as
            # well, but we remove it
            real = [self.vertices[i] for i in indices[:-1]]
            realCycles.append(real)
        return realCycles
