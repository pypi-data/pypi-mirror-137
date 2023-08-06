import pytest

import kep_solver.fileio as fileio
from kep_solver.entities import BloodGroup


@pytest.fixture(params=[
    ("JSON", fileio.read_json("tests/test_instances/test1.json")),
    ("XML", fileio.read_xml("tests/test_instances/test1.xml"))
])
def test_one(request):
    yield request.param


def test_instance_one(test_one):
    instance = test_one[1]
    assert len(instance.donors()) == 4
    assert len(instance.transplants()) == 5
    firstDonor = instance.donor("1")
    assert firstDonor.age == 50
    assert firstDonor.recipient.id == "1"
    assert firstDonor.bloodGroup == BloodGroup.O
    assert len(firstDonor.transplants()) == 1
    assert instance.recipient("1").pairedWith(firstDonor)
    assert not instance.recipient("2").pairedWith(firstDonor)
    transplant = firstDonor.transplants()[0]
    assert transplant.donor.id == "1"
    assert transplant.recipient.id == "2"
    assert transplant.weight == 1
    secondDonor = instance.donor("2")
    assert secondDonor.age == 50
    assert secondDonor.recipient.id == "2"
    assert secondDonor.bloodGroup == BloodGroup.A
    assert len(secondDonor.transplants()) == 2
    thirdDonor = instance.donor("3")
    assert thirdDonor.age == 60
    assert thirdDonor.recipient.id == "3"
    assert thirdDonor.bloodGroup == BloodGroup.AB
    assert len(thirdDonor.transplants()) == 1
    # Only JSON can store patient information
    if test_one[0] == "JSON":
        assert firstDonor.recipient.bloodGroup == BloodGroup.O
        assert firstDonor.recipient.cPRA == 0.25
        assert secondDonor.recipient.bloodGroup == BloodGroup.B
        assert secondDonor.recipient.cPRA == 0
        assert thirdDonor.recipient.bloodGroup == BloodGroup.O
        assert thirdDonor.recipient.cPRA == 0.98
        fourthDonor = instance.donor("4")
        assert fourthDonor.recipient.bloodGroup == BloodGroup.AB
        assert fourthDonor.recipient.cPRA == 0.10
        assert instance.recipient("1").hasBloodCompatibleDonor()
        assert not instance.recipient("3").hasBloodCompatibleDonor()


# A bit less stringent checking on these instances

@pytest.fixture(params=[
    ("JSON", fileio.read_json("tests/test_instances/test2.json")),
    ("XML", fileio.read_xml("tests/test_instances/test2.xml"))
])
def test_two(request):
    yield request.param


def test_instance_two(test_two):
    instance = test_two[1]
    assert len(instance.donors()) == 6
    assert len(instance.transplants()) == 10
    assert len(instance.donor("5").transplants()) == 2


@pytest.fixture(params=[
    ("JSON", fileio.read_json("tests/test_instances/test3.json")),
    ("XML", fileio.read_xml("tests/test_instances/test3.xml"))
])
def test_three(request):
    yield request.param


def test_instance_three(test_three):
    instance = test_three[1]
    assert len(instance.donors()) == 3
    assert len(instance.transplants()) == 4
    assert len(instance.donor("1").transplants()) == 2


@pytest.fixture(params=[
    ("JSON", fileio.read_json("tests/test_instances/test3b.json")),
    ("XML", fileio.read_xml("tests/test_instances/test3b.xml"))
])
def test_threeb(request):
    yield request.param


def test_instance_threeb(test_threeb):
    instance = test_threeb[1]
    assert len(instance.donors()) == 4
    assert len(instance.transplants()) == 9
    assert len(instance.donor("1").transplants()) == 3


@pytest.fixture(params=[
    ("JSON", fileio.read_json("tests/test_instances/test4.json")),
    ("XML", fileio.read_xml("tests/test_instances/test4.xml"))
])
def test_four(request):
    yield request.param


def test_instance_four(test_four):
    instance = test_four[1]
    assert len(instance.donors()) == 4
    assert len(instance.transplants()) == 6
    assert len(instance.donor("4").transplants()) == 2
    assert instance.transplants()[0].weight == 4


@pytest.fixture(params=[
    ("JSON", fileio.read_json("tests/test_instances/test5.json")),
    ("XML", fileio.read_xml("tests/test_instances/test5.xml"))
])
def test_five(request):
    yield request.param


def test_instance_five(test_five):
    instance = test_five[1]
    assert len(instance.donors()) == 4
    assert len(instance.transplants()) == 4
    ndd = instance.donor("1")
    assert ndd.NDD
    with pytest.raises(Exception):
        ndd.recipient()
    directed = instance.donor("2")
    assert not directed.NDD
    recip = directed.recipient
    assert not recip.pairedWith(ndd)
    assert recip.pairedWith(directed)
    assert recip.id == "2"
