import pytest

import kep_solver.fileio as fileio
from kep_solver.graph import CompatibilityGraph


@pytest.fixture(params=[
    ("JSON", fileio.read_json("tests/test_instances/test1.json")),
    ("XML", fileio.read_xml("tests/test_instances/test1.xml"))
])
def test_one(request):
    yield request.param


def test_instance_one_read(test_one):
    instance = test_one[1]
    graph = CompatibilityGraph(instance)
    assert graph.size == 4
    assert len(graph.edges()) == len(instance.transplants())


def test_instance_one_cycles(test_one):
    instance = test_one[1]
    graph = CompatibilityGraph(instance)

    cycles = graph.findCycles(3)
    assert len(cycles) == 2
    cycle_indices = [[v.index for v in cycle] for cycle in cycles]
    assert [0, 1] in cycle_indices
    assert [1, 2, 3] in cycle_indices

    cycles = graph.findCycles(2)
    cycle_indices = [[v.index for v in cycle] for cycle in cycles]
    assert [0, 1] in cycle_indices
    assert len(cycles) == 1


@pytest.fixture(params=[
    ("JSON", fileio.read_json("tests/test_instances/test2.json")),
    ("XML", fileio.read_xml("tests/test_instances/test2.xml"))
])
def test_two(request):
    yield request.param


def test_instance_two_read(test_two):
    instance = test_two[1]
    graph = CompatibilityGraph(instance)
    assert graph.size == 6
    assert len(graph.edges()) == len(instance.transplants())


def test_instance_two_cycles(test_two):
    instance = test_two[1]
    graph = CompatibilityGraph(instance)

    cycles = graph.findCycles(3)
    assert len(cycles) == 5
    cycle_indices = [[int(v.donor.id) for v in cycle] for cycle in cycles]
    assert [1, 2] in cycle_indices
    assert [3, 4] in cycle_indices
    assert [5, 6] in cycle_indices
    assert [1, 4, 2] in cycle_indices
    assert [3, 6, 5] in cycle_indices
    cycle = [graph.vertices[0], graph.vertices[3], graph.vertices[1]]
    assert graph.numBackArcs(cycle) == 1
    cycle = [graph.vertices[2], graph.vertices[5], graph.vertices[4]]
    assert graph.numBackArcs(cycle) == 1

    cycles = graph.findCycles(2)
    assert len(cycles) == 3
    cycle_indices = [[int(v.donor.id) for v in cycle] for cycle in cycles]
    assert [1, 2] in cycle_indices
    assert [3, 4] in cycle_indices
    assert [5, 6] in cycle_indices


def test_instance_two_embedded(test_two):
    instance = test_two[1]
    graph = CompatibilityGraph(instance)
    cycle = [graph.vertices[0], graph.vertices[3], graph.vertices[1]]
    embedded = graph.embeddedExchanges(cycle)
    assert embedded[0] == [graph.vertices[0], graph.vertices[1]]
    cycle = [graph.vertices[2], graph.vertices[5], graph.vertices[4]]
    embedded = graph.embeddedExchanges(cycle)
    assert embedded[0] == [graph.vertices[5], graph.vertices[4]]
    cycles = graph.findCycles(3)
    for cycle in cycles:
        if len(cycle) == 2:
            assert len(graph.embeddedExchanges(cycle)) == 0


@pytest.fixture(params=[
    ("JSON", fileio.read_json("tests/test_instances/test5.json")),
    ("XML", fileio.read_xml("tests/test_instances/test5.xml"))
])
def test_five(request):
    yield request.param


def test_instance_five_read(test_five):
    instance = test_five[1]
    graph = CompatibilityGraph(instance)
    assert graph.size == 4
    assert len(graph.edges()) == len(instance.transplants())


def test_instance_five_chains(test_five):
    instance = test_five[1]
    graph = CompatibilityGraph(instance)
    chains = graph.findChains(2)
    assert(len(chains) == 3)
    chain_indices = [[int(v.donor.id) for v in chain] for chain in chains]
    assert [1] in chain_indices
    assert [1, 2] in chain_indices
    assert [1, 3] in chain_indices

    chains = graph.findChains(3)
    assert(len(chains) == 4)
    chain_indices = [[int(v.donor.id) for v in chain] for chain in chains]
    assert [1] in chain_indices
    assert [1, 2] in chain_indices
    assert [1, 3] in chain_indices
    assert [1, 3, 4] in chain_indices


def test_cycle_finding_medium1():
    instance = fileio.read_json("tests/test_instances/medium-1.json")
    graph = CompatibilityGraph(instance)

    cycles = graph.findCycles(3)
    cycles += graph.findChains(3)
    assert len([c for c in cycles if len(c) == 2]) == 66
    assert len([c for c in cycles if len(c) == 3]) == 191


def test_cycle_finding_medium2():
    instance = fileio.read_json("tests/test_instances/medium-2.json")
    graph = CompatibilityGraph(instance)

    cycles = graph.findCycles(3)
    cycles += graph.findChains(3)
    assert len([c for c in cycles if len(c) == 2]) == 68
    assert len([c for c in cycles if len(c) == 3]) == 199


def test_cycle_finding_medium3():
    instance = fileio.read_json("tests/test_instances/medium-3.json")
    graph = CompatibilityGraph(instance)

    cycles = graph.findCycles(3)
    cycles += graph.findChains(3)
    assert len([c for c in cycles if len(c) == 2]) == 55
    assert len([c for c in cycles if len(c) == 3]) == 180


def test_cycle_finding_medium4():
    instance = fileio.read_json("tests/test_instances/medium-4.json")
    graph = CompatibilityGraph(instance)

    cycles = graph.findCycles(3)
    cycles += graph.findChains(3)
    assert len([c for c in cycles if len(c) == 2]) == 28
    assert len([c for c in cycles if len(c) == 3]) == 95


def test_cycle_finding_medium5():
    instance = fileio.read_json("tests/test_instances/medium-5.json")
    graph = CompatibilityGraph(instance)

    cycles = graph.findCycles(3)
    cycles += graph.findChains(3)
    assert len([c for c in cycles if len(c) == 2]) == 58
    assert len([c for c in cycles if len(c) == 3]) == 193


def test_cycle_finding_medium6():
    instance = fileio.read_json("tests/test_instances/medium-6.json")
    graph = CompatibilityGraph(instance)

    cycles = graph.findCycles(3)
    cycles += graph.findChains(3)
    assert len([c for c in cycles if len(c) == 2]) == 41
    assert len([c for c in cycles if len(c) == 3]) == 142


def test_cycle_finding_medium7():
    instance = fileio.read_json("tests/test_instances/medium-7.json")
    graph = CompatibilityGraph(instance)

    cycles = graph.findCycles(3)
    cycles += graph.findChains(3)
    assert len([c for c in cycles if len(c) == 2]) == 48
    assert len([c for c in cycles if len(c) == 3]) == 163


def test_cycle_finding_medium8():
    instance = fileio.read_json("tests/test_instances/medium-8.json")
    graph = CompatibilityGraph(instance)

    cycles = graph.findCycles(3)
    cycles += graph.findChains(3)
    assert len([c for c in cycles if len(c) == 2]) == 41
    assert len([c for c in cycles if len(c) == 3]) == 92


def test_cycle_finding_medium9():
    instance = fileio.read_json("tests/test_instances/medium-9.json")
    graph = CompatibilityGraph(instance)

    cycles = graph.findCycles(3)
    cycles += graph.findChains(3)
    assert len([c for c in cycles if len(c) == 2]) == 79
    assert len([c for c in cycles if len(c) == 3]) == 373


def test_cycle_finding_medium10():
    instance = fileio.read_json("tests/test_instances/medium-10.json")
    graph = CompatibilityGraph(instance)

    cycles = graph.findCycles(3)
    cycles += graph.findChains(3)
    assert len([c for c in cycles if len(c) == 2]) == 56
    assert len([c for c in cycles if len(c) == 3]) == 156


def test_cycle_finding_large1():
    instance = fileio.read_json("tests/test_instances/large-1.json")
    graph = CompatibilityGraph(instance)

    cycles = graph.findCycles(3)
    cycles += graph.findChains(3)
    assert len([c for c in cycles if len(c) == 2]) == 696
    assert len([c for c in cycles if len(c) == 3]) == 6837


def test_cycle_finding_large2():
    instance = fileio.read_json("tests/test_instances/large-2.json")
    graph = CompatibilityGraph(instance)

    cycles = graph.findCycles(3)
    cycles += graph.findChains(3)
    assert len([c for c in cycles if len(c) == 2]) == 915
    assert len([c for c in cycles if len(c) == 3]) == 12175


def test_cycle_finding_large3():
    instance = fileio.read_json("tests/test_instances/large-3.json")
    graph = CompatibilityGraph(instance)

    cycles = graph.findCycles(3)
    cycles += graph.findChains(3)
    assert len([c for c in cycles if len(c) == 2]) == 930
    assert len([c for c in cycles if len(c) == 3]) == 13639


def test_cycle_finding_large4():
    instance = fileio.read_json("tests/test_instances/large-4.json")
    graph = CompatibilityGraph(instance)

    cycles = graph.findCycles(3)
    cycles += graph.findChains(3)
    assert len([c for c in cycles if len(c) == 2]) == 857
    assert len([c for c in cycles if len(c) == 3]) == 11761


def test_cycle_finding_large5():
    instance = fileio.read_json("tests/test_instances/large-5.json")
    graph = CompatibilityGraph(instance)

    cycles = graph.findCycles(3)
    cycles += graph.findChains(3)
    assert len([c for c in cycles if len(c) == 2]) == 835
    assert len([c for c in cycles if len(c) == 3]) == 12407


def test_cycle_finding_large6():
    instance = fileio.read_json("tests/test_instances/large-6.json")
    graph = CompatibilityGraph(instance)

    cycles = graph.findCycles(3)
    cycles += graph.findChains(3)
    assert len([c for c in cycles if len(c) == 2]) == 1070
    assert len([c for c in cycles if len(c) == 3]) == 13766


def test_cycle_finding_large7():
    instance = fileio.read_json("tests/test_instances/large-7.json")
    graph = CompatibilityGraph(instance)

    cycles = graph.findCycles(3)
    cycles += graph.findChains(3)
    assert len([c for c in cycles if len(c) == 2]) == 931
    assert len([c for c in cycles if len(c) == 3]) == 11139


def test_cycle_finding_large8():
    instance = fileio.read_json("tests/test_instances/large-8.json")
    graph = CompatibilityGraph(instance)

    cycles = graph.findCycles(3)
    cycles += graph.findChains(3)
    assert len([c for c in cycles if len(c) == 2]) == 1202
    assert len([c for c in cycles if len(c) == 3]) == 18319


def test_cycle_finding_large9():
    instance = fileio.read_json("tests/test_instances/large-9.json")
    graph = CompatibilityGraph(instance)

    cycles = graph.findCycles(3)
    cycles += graph.findChains(3)
    assert len([c for c in cycles if len(c) == 2]) == 1167
    assert len([c for c in cycles if len(c) == 3]) == 15610


def test_cycle_finding_large10():
    instance = fileio.read_json("tests/test_instances/large-10.json")
    graph = CompatibilityGraph(instance)

    cycles = graph.findCycles(3)
    cycles += graph.findChains(3)
    assert len([c for c in cycles if len(c) == 2]) == 1013
    assert len([c for c in cycles if len(c) == 3]) == 14655
