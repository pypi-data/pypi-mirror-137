"""This module contains file IO functions."""

import json
from defusedxml import ElementTree as ET  # type: ignore

from kep_solver.entities import Instance, Donor, Transplant


def read_json(filename: str) -> Instance:
    """Read an instance in JSON format from the given file

    :param filename: The name of the file containing the JSON instance
    :return: the corresponding Instance
    """
    with open(filename, "r") as infile:
        return parse_json(infile.read())


def parse_json(jsonstring: str) -> Instance:
    """Read an instance in JSON format from the given string

    :param jsonstring: A string holding a JSON representation of
        the instance
    :return: the corresponding Instance
    """
    json_obj = json.loads(jsonstring)
    instance = Instance()
    data = json_obj["data"]
    for donor_id, donor_data in data.items():
        donor = Donor(donor_id)
        if "dage" in donor_data:
            donor.age = float(donor_data["dage"])
        if "bloodtype" in donor_data:
            donor.bloodGroup = donor_data["bloodtype"]
        if "sources" not in donor_data:
            donor.NDD = True
        elif len(donor_data["sources"]) == 0:
            donor.NDD = True
        elif len(donor_data["sources"]) != 1:
            raise Exception("Donor with more than one recipient detected")
        else:
            recip = instance.recipient(str(donor_data["sources"][0]))
            donor.recipient = recip
            recip.addDonor(donor)
        instance.addDonor(donor)
        if "matches" in donor_data:
            for arc in donor_data["matches"]:
                recip = instance.recipient(str(arc["recipient"]))
                t = Transplant(donor, recip, float(arc["score"]))
                instance.addTransplant(t)
    if "recipients" in json_obj:
        recips = json_obj["recipients"]
        for rid, info in recips.items():
            recip = instance.recipient(str(rid))
            if "pra" in info:
                recip.cPRA = float(info["pra"])
            if "cPRA" in info:
                recip.cPRA = float(info["cPRA"])
            if "bloodgroup" in info:
                recip.bloodGroup = info["bloodgroup"]
            if "bloodtype" in info:
                recip.bloodGroup = info["bloodtype"]
    return instance


def read_xml(filename: str) -> Instance:
    """Read an instance in XML format from the given file

    :param filename: The name of the file containing the XML instance
    :return: the corresponding Instance
    """
    with open(filename, "r") as infile:
        return parse_xml(infile.read())


def parse_xml(xmlstring: str) -> Instance:
    """Read an instance in XML format from the given string

    :param xmlstring: A string holding a XML representation of
        the instance
    :return: the corresponding Instance
    """
    xml = ET.fromstring(xmlstring)
    instance = Instance()
    for donor_xml in xml:
        donor = Donor(donor_xml.attrib["donor_id"])
        age_xml = donor_xml.find("dage")
        if age_xml is not None:
            donor.age = float(age_xml.text)
        bloodgroup_xml = donor_xml.find("bloodgroup")
        if bloodgroup_xml is not None:
            donor.bloodGroup = bloodgroup_xml.text
        sources = donor_xml.find("sources")
        if sources is not None:
            if len(sources) == 0:
                donor.NDD = True
            elif len(sources) != 1:
                raise Exception("Donor with more than one recipient detected")
            recip = instance.recipient(str(sources[0].text))
            donor.recipient = recip
            recip.addDonor(donor)
        else:
            donor.NDD = True
        instance.addDonor(donor)
        matches = donor_xml.find("matches")
        if matches is not None:
            for match in matches:
                recip = instance.recipient(str(match.find("recipient").text))
                score = float(match.find("score").text)
                t = Transplant(donor, recip, score)
                instance.addTransplant(t)
    return instance


def read_file(filename: str) -> Instance:
    """Read a file containing a KEP instance. Will attempt to detect the
    correct file format if possible.

    :param filename: The name of the file containing the instance
    :return: the corresponding Instance
    """
    if filename[-4:] == ".xml":
        return read_xml(filename)
    if filename[-5:] == ".json":
        return read_json(filename)
    raise Exception(f"Unknown filetype: {filename}")
