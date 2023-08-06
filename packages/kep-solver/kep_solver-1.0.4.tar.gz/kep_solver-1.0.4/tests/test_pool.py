import pytest

import kep_solver.model as model
import kep_solver.pool as pool
import kep_solver.fileio as fileio


@pytest.fixture(scope='module')
def transplant_pool():
    obj = model.TransplantCount()
    return pool.Pool([obj])


def test_transplant_count_test1(transplant_pool):
    instance = fileio.read_json("tests/test_instances/test1.json")
    solution = transplant_pool.solve_single(instance)
    assert solution.values[0] == 3


def test_transplant_count_possible(transplant_pool):
    for testfile in [
                     "tests/test_instances/test1.json",
                     "tests/test_instances/test2.json",
                     "tests/test_instances/test3.json",
                     "tests/test_instances/test3b.json",
                     "tests/test_instances/test4.json",
                     "tests/test_instances/test5.json",
                     ]:
        instance = fileio.read_json(testfile)
        solution = transplant_pool.solve_single(instance)
        for exchange in solution.possible:
            assert len(exchange.vertices) == exchange.values[0]


def test_transplant_count_test2(transplant_pool):
    instance = fileio.read_json("tests/test_instances/test2.json")
    solution = transplant_pool.solve_single(instance)
    assert solution.values[0] == 6


def test_transplant_count_test3(transplant_pool):
    instance = fileio.read_json("tests/test_instances/test3.json")
    solution = transplant_pool.solve_single(instance)
    assert solution.values[0] == 3


def test_transplant_count_test3b(transplant_pool):
    instance = fileio.read_json("tests/test_instances/test3b.json")
    solution = transplant_pool.solve_single(instance)
    assert solution.values[0] == 4


def test_transplant_count_test4(transplant_pool):
    instance = fileio.read_json("tests/test_instances/test4.json")
    solution = transplant_pool.solve_single(instance)
    assert solution.values[0] == 3


def test_transplant_count_test5(transplant_pool):
    instance = fileio.read_json("tests/test_instances/test5.json")
    solution = transplant_pool.solve_single(instance)
    assert solution.values[0] == 4


def test_transplant_count_medium1(transplant_pool):
    instance = fileio.read_json("tests/test_instances/medium-1.json")
    solution = transplant_pool.solve_single(instance)
    assert solution.values[0] == 23


def test_transplant_count_medium2(transplant_pool):
    instance = fileio.read_json("tests/test_instances/medium-2.json")
    solution = transplant_pool.solve_single(instance)
    assert solution.values[0] == 22


def test_transplant_count_medium3(transplant_pool):
    instance = fileio.read_json("tests/test_instances/medium-3.json")
    solution = transplant_pool.solve_single(instance)
    assert solution.values[0] == 22


def test_transplant_count_medium4(transplant_pool):
    instance = fileio.read_json("tests/test_instances/medium-4.json")
    solution = transplant_pool.solve_single(instance)
    assert solution.values[0] == 19


def test_transplant_count_medium5(transplant_pool):
    instance = fileio.read_json("tests/test_instances/medium-5.json")
    solution = transplant_pool.solve_single(instance)
    assert solution.values[0] == 23


def test_transplant_count_medium6(transplant_pool):
    instance = fileio.read_json("tests/test_instances/medium-6.json")
    solution = transplant_pool.solve_single(instance)
    assert solution.values[0] == 23


def test_transplant_count_medium7(transplant_pool):
    instance = fileio.read_json("tests/test_instances/medium-7.json")
    solution = transplant_pool.solve_single(instance)
    assert solution.values[0] == 23


def test_transplant_count_medium8(transplant_pool):
    instance = fileio.read_json("tests/test_instances/medium-8.json")
    solution = transplant_pool.solve_single(instance)
    assert solution.values[0] == 18


def test_transplant_count_medium9(transplant_pool):
    instance = fileio.read_json("tests/test_instances/medium-9.json")
    solution = transplant_pool.solve_single(instance)
    assert solution.values[0] == 30


def test_transplant_count_medium10(transplant_pool):
    instance = fileio.read_json("tests/test_instances/medium-10.json")
    solution = transplant_pool.solve_single(instance)
    assert solution.values[0] == 21


def test_transplant_count_large1(transplant_pool):
    instance = fileio.read_json("tests/test_instances/large-1.json")
    solution = transplant_pool.solve_single(instance)
    assert solution.values[0] == 146


def test_transplant_count_large2(transplant_pool):
    instance = fileio.read_json("tests/test_instances/large-2.json")
    solution = transplant_pool.solve_single(instance)
    assert solution.values[0] == 168


def test_transplant_count_large3(transplant_pool):
    instance = fileio.read_json("tests/test_instances/large-3.json")
    solution = transplant_pool.solve_single(instance)
    assert solution.values[0] == 161


def test_transplant_count_large4(transplant_pool):
    instance = fileio.read_json("tests/test_instances/large-4.json")
    solution = transplant_pool.solve_single(instance)
    assert solution.values[0] == 149


def test_transplant_count_large5(transplant_pool):
    instance = fileio.read_json("tests/test_instances/large-5.json")
    solution = transplant_pool.solve_single(instance)
    assert solution.values[0] == 162


def test_transplant_count_large6(transplant_pool):
    instance = fileio.read_json("tests/test_instances/large-6.json")
    solution = transplant_pool.solve_single(instance)
    assert solution.values[0] == 152


def test_transplant_count_large7(transplant_pool):
    instance = fileio.read_json("tests/test_instances/large-7.json")
    solution = transplant_pool.solve_single(instance)
    assert solution.values[0] == 154


def test_transplant_count_large8(transplant_pool):
    instance = fileio.read_json("tests/test_instances/large-8.json")
    solution = transplant_pool.solve_single(instance)
    assert solution.values[0] == 176


def test_transplant_count_large9(transplant_pool):
    instance = fileio.read_json("tests/test_instances/large-9.json")
    solution = transplant_pool.solve_single(instance)
    assert solution.values[0] == 174


def test_transplant_count_large10(transplant_pool):
    instance = fileio.read_json("tests/test_instances/large-10.json")
    solution = transplant_pool.solve_single(instance)
    assert solution.values[0] == 158


@pytest.fixture(scope='module')
def twoway_pool():
    obj = model.EffectiveTwoWay()
    return pool.Pool([obj])


def test_effective_twoway_count_test1(twoway_pool):
    instance = fileio.read_json("tests/test_instances/test1.json")
    solution = twoway_pool.solve_single(instance)
    assert solution.values[0] == 1


def test_effective_twoway_count_test2(twoway_pool):
    instance = fileio.read_json("tests/test_instances/test2.json")
    solution = twoway_pool.solve_single(instance)
    assert solution.values[0] == 3


def test_effective_twoway_count_test3(twoway_pool):
    instance = fileio.read_json("tests/test_instances/test3.json")
    solution = twoway_pool.solve_single(instance)
    assert solution.values[0] == 1


def test_effective_twoway_count_test3b(twoway_pool):
    instance = fileio.read_json("tests/test_instances/test3b.json")
    solution = twoway_pool.solve_single(instance)
    assert solution.values[0] == 2


def test_effective_twoway_count_test4(twoway_pool):
    instance = fileio.read_json("tests/test_instances/test4.json")
    solution = twoway_pool.solve_single(instance)
    assert solution.values[0] == 1


def test_effective_twoway_count_test5(twoway_pool):
    instance = fileio.read_json("tests/test_instances/test5.json")
    solution = twoway_pool.solve_single(instance)
    assert solution.values[0] == 1


@pytest.fixture(scope='module')
def backarc_pool():
    obj = model.BackArcs()
    return pool.Pool([obj])


def test_backarcs_test3(backarc_pool):
    instance = fileio.read_json("tests/test_instances/test3b.json")
    solution = backarc_pool.solve_single(instance)
    assert solution.values[0] == 3


def test_backarcs_test5(backarc_pool):
    instance = fileio.read_json("tests/test_instances/test5.json")
    solution = backarc_pool.solve_single(instance)
    assert solution.values[0] == 2


@pytest.fixture(scope='module')
def threeway_pool():
    obj = model.ThreeWay()
    return pool.Pool([obj])


def test_threeway_count_test1(threeway_pool):
    instance = fileio.read_json("tests/test_instances/test1.json")
    solution = threeway_pool.solve_single(instance)
    assert solution.values[0] == 0
