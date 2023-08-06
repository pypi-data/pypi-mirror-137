import pytest

import kep_solver.model as model
import kep_solver.graph as graphing
import kep_solver.fileio as fileio


@pytest.fixture(scope='module')
def test1_graph():
    instance = fileio.read_json("tests/test_instances/test1.json")
    graph = graphing.CompatibilityGraph(instance)
    return graph


@pytest.fixture(scope='module')
def test3b_graph():
    instance = fileio.read_json("tests/test_instances/test3b.json")
    graph = graphing.CompatibilityGraph(instance)
    return graph


@pytest.fixture(scope='module')
def test4_graph():
    instance = fileio.read_json("tests/test_instances/test4.json")
    graph = graphing.CompatibilityGraph(instance)
    return graph


@pytest.fixture(scope='module')
def test5_graph():
    instance = fileio.read_json("tests/test_instances/test5.json")
    graph = graphing.CompatibilityGraph(instance)
    return graph


def test_transplant_count_test1(test1_graph):
    obj = model.TransplantCount()
    cycle = [test1_graph.vertices[0], test1_graph.vertices[1]]
    assert obj.value(test1_graph, cycle) == 2
    cycle = [test1_graph.vertices[1], test1_graph.vertices[2],
             test1_graph.vertices[3]]
    assert obj.value(test1_graph, cycle) == 3


def test_transplant_count_test5(test5_graph):
    obj = model.TransplantCount()
    cycle = [test5_graph.vertices[0], test5_graph.vertices[1]]
    assert obj.value(test5_graph, cycle) == 2
    cycle = [test5_graph.vertices[0], test5_graph.vertices[2],
             test5_graph.vertices[3]]
    assert obj.value(test5_graph, cycle) == 3


def test_effective_twoway_count_test1(test1_graph):
    obj = model.EffectiveTwoWay()
    cycle = [test1_graph.vertices[0], test1_graph.vertices[1]]
    assert obj.value(test1_graph, cycle) == 1
    cycle = [test1_graph.vertices[1], test1_graph.vertices[2],
             test1_graph.vertices[3]]
    assert obj.value(test1_graph, cycle) == 0


def test_effective_twoway_count_test4(test4_graph):
    obj = model.EffectiveTwoWay()
    cycle = [test4_graph.vertices[0], test4_graph.vertices[1]]
    assert obj.value(test4_graph, cycle) == 1
    cycle = [test4_graph.vertices[0], test4_graph.vertices[1],
             test4_graph.vertices[3]]
    assert obj.value(test4_graph, cycle) == 1
    cycle = [test4_graph.vertices[1], test4_graph.vertices[3],
             test4_graph.vertices[2]]
    assert obj.value(test4_graph, cycle) == 0


def test_backarcs_test3b(test3b_graph):
    obj = model.BackArcs()
    cycle = [test3b_graph.vertices[0], test3b_graph.vertices[1]]
    assert obj.value(test3b_graph, cycle) == 0
    cycle = [test3b_graph.vertices[0], test3b_graph.vertices[1],
             test3b_graph.vertices[2]]
    assert obj.value(test3b_graph, cycle) == 2
    cycle = [test3b_graph.vertices[0], test3b_graph.vertices[2],
             test3b_graph.vertices[3]]
    assert obj.value(test3b_graph, cycle) == 3


def test_backarcs_test5(test5_graph):
    obj = model.BackArcs()
    cycle = [test5_graph.vertices[0], test5_graph.vertices[1]]
    assert obj.value(test5_graph, cycle) == 0
    cycle = [test5_graph.vertices[0], test5_graph.vertices[2],
             test5_graph.vertices[3]]
    assert obj.value(test5_graph, cycle) == 2


def test_threeway_count_test1(test1_graph):
    obj = model.ThreeWay()
    cycle = [test1_graph.vertices[0], test1_graph.vertices[1]]
    assert obj.value(test1_graph, cycle) == 0
    cycle = [test1_graph.vertices[1], test1_graph.vertices[2],
             test1_graph.vertices[3]]
    assert obj.value(test1_graph, cycle) == 1


def test_threeway_count_test5(test5_graph):
    obj = model.ThreeWay()
    cycle = [test5_graph.vertices[0], test5_graph.vertices[1]]
    assert obj.value(test5_graph, cycle) == 0
    cycle = [test5_graph.vertices[0], test5_graph.vertices[1],
             test5_graph.vertices[3]]
    assert obj.value(test5_graph, cycle) == 1
    cycle = [test5_graph.vertices[1], test5_graph.vertices[3],
             test5_graph.vertices[2]]
    assert obj.value(test5_graph, cycle) == 1
