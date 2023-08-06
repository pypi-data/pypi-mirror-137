"""This module contains entities (such as Donors, Recipients) within
a KEP, as well as the encapsulating Instance objects
"""

from __future__ import annotations

from collections.abc import ValuesView
from enum import Enum
from typing import Optional


class KEPDataValidationException(Exception):
    """An exception that is raised when invalid data requests are made.
    This can happen if properties (such as blood group or cPRA) are
    requested when they are not known, or if changes are attempted on
    such properties.
    """

    pass


class BloodGroup(Enum):
    """The blood group of a participant in a KEP."""

    O = 0  # noqa: E741
    A = 1
    B = 2
    AB = 3

    def __str__(self):
        return _BG_TO_STR[self]


_BLOODGROUPS = {
    "O": BloodGroup.O,
    "A": BloodGroup.A,
    "B": BloodGroup.B,
    "AB": BloodGroup.AB,
}

_BG_TO_STR = {
    BloodGroup.O: "O",
    BloodGroup.A: "A",
    BloodGroup.B: "B",
    BloodGroup.AB: "AB",
}


def parseBloodGroup(bloodGroupText: str) -> BloodGroup:
    """Given a blood group as text, return the corresponding
    BloodGroup object.

    :param bloodGroupText: the text
    :return: the BloodGroup
    """
    if bloodGroupText not in _BLOODGROUPS:
        raise Exception(f"Unknown blood group: {bloodGroupText}")
    return _BLOODGROUPS[bloodGroupText]


class Recipient:
    """A recipient in a KEP instance."""

    def __init__(self, id: str):
        self._id: str = id
        self._age: Optional[float] = None
        self._cPRA: Optional[float] = None
        self._bloodGroup: Optional[BloodGroup] = None
        self._donors: list[Donor] = []

    def __str__(self):
        return f"R{self._id}"

    def longstr(self):
        """A longer string representation.

        :return: a string representation
        """
        return f"Recipient {self._id}"

    def __hash__(self):
        return hash(f"R{self._id}")

    @property
    def id(self) -> str:
        """Return the ID of this recipient."""
        return self._id

    @property
    def age(self) -> float:
        """The age of this recipient (in years), fractions allowed."""
        if self._age is None:
            raise KEPDataValidationException(f"Age of {str(self)} not known")
        return self._age

    @age.setter
    def age(self, age: float) -> None:
        if self._age is not None and self._age != age:
            raise KEPDataValidationException(f"Trying to change age of {str(self)}")
        self._age = age

    @property
    def cPRA(self) -> float:
        """The cPRA of this recipient, as a value between 0 and 1."""
        if self._cPRA is None:
            raise KEPDataValidationException(f"cPRA of {str(self)} not known")
        return self._cPRA

    @cPRA.setter
    def cPRA(self, cPRA: float) -> None:
        if self._cPRA is not None and self._cPRA != cPRA:
            raise KEPDataValidationException(f"Trying to change cPRA of {str(self)}")
        if cPRA > 1 or cPRA < 0:
            raise KEPDataValidationException(
                f"Trying to set the cPRA of {str(self)} to an invalid value."
            )
        self._cPRA = cPRA

    @property
    def bloodGroup(self) -> BloodGroup:
        """The blood group of this recipient."""
        if self._bloodGroup is None:
            raise KEPDataValidationException(f"Blood group of {str(self)} not known")
        return self._bloodGroup

    @bloodGroup.setter
    def bloodGroup(self, bloodGroup: str) -> None:
        group = parseBloodGroup(bloodGroup)
        if self._bloodGroup is not None and self._bloodGroup != group:
            raise KEPDataValidationException(
                f"Trying to change blood group of {str(self)}"
            )
        self._bloodGroup = group

    def addDonor(self, donor: Donor) -> None:
        """Add a paired donor for this recipient.

        :param donor: The donor to add
        """
        self._donors.append(donor)

    def donors(self) -> list[Donor]:
        """The list of donors paired with this recipient

        :return: the list of donors
        """
        return self._donors

    def hasBloodCompatibleDonor(self) -> bool:
        """Return true if the recipient is paired with at least one
        donor who is blood-group compatible with this recipient.

        :return: true if the recipient has a blood-group compatible
            donor
        """
        for donor in self.donors():
            if donor.bloodGroupCompatible(self):
                return True
        return False

    def pairedWith(self, donor: Donor) -> bool:
        """Return true if the given donor is paired with this recipient.

        :param donor: The donor in question
        :return: true if the donor is paired with this recipient
        """
        return donor in self.donors()


class Donor:
    """A donor (directed or non-directed) in an instance."""

    def __init__(self, id: str):
        """Construct a Donor object. These are assumed to be
        directed, this can be changed with the NDD instance variable.

        :param id: An identifier for this donor.
        """
        self._id: str = id
        self._recip: Optional[Recipient] = None
        self.NDD: bool = False
        self._age: Optional[float] = None
        self._bloodGroup: Optional[BloodGroup] = None
        self._outgoingTransplants: list["Transplant"] = []

    def __eq__(self, other):
        # An instance can only have one donor of each ID.
        return self.id == other.id

    def __str__(self):
        if self.NDD:
            return f"NDD{self._id}"
        return f"D{self._id}"

    def longstr(self):
        """A longer string representation.

        :return: a string representation
        """
        if self.NDD:
            return f"Non-directed donor {self._id}"
        return f"Donor {self._id}"

    def __hash__(self):
        return hash(f"D{self._id}")

    @property
    def id(self) -> str:
        """Return the ID of this donor."""
        return self._id

    @property
    def age(self) -> float:
        """The age of the donor (in years), fractions allowed."""
        if self._age is None:
            raise KEPDataValidationException(f"Age of donor {self.id} not known")
        return self._age

    @age.setter
    def age(self, age: float) -> None:
        if self._age is not None and self._age != age:
            raise KEPDataValidationException(
                f"Trying to change age of donor {self.id}"
            )
        self._age = age

    @property
    def bloodGroup(self) -> BloodGroup:
        """The donors blood group"""
        if self._bloodGroup is None:
            raise KEPDataValidationException(f"Blood group of {str(self)} not known")
        return self._bloodGroup

    @bloodGroup.setter
    def bloodGroup(self, bloodGroup: str) -> None:
        group = parseBloodGroup(bloodGroup)
        if self._bloodGroup is not None and self._bloodGroup != group:
            raise KEPDataValidationException(
                f"Trying to change blood group of {str(self)}"
            )
        self._bloodGroup = group

    @property
    def recipient(self) -> Recipient:
        """The recipient paired with this donor."""
        if self.NDD:
            raise KEPDataValidationException(
                f"Tried to get recipient of non-directed donor {str(self)}."
            )
        if not self._recip:
            raise KEPDataValidationException(
                f"Donor {str(self)} is directed but has no recipient."
            )
        return self._recip

    @recipient.setter
    def recipient(self, new_recip: Recipient) -> None:
        if self._recip is not None:
            raise KEPDataValidationException(
                f"Tried to set a second recipient on donor {str(self)}"
            )
        if self.NDD:
            raise KEPDataValidationException(
                f"Tried to set recipient of non-directed donor {str(self)}."
            )
        self._recip = new_recip

    def bloodGroupCompatible(self, recipient: Recipient) -> bool:
        """Is this donor blood-group compatible with the given
        recipient.

        :param recipient: the recipient in question
        :return: True if the donor is blood-group compatible with the
            given recipient
        """
        if self.bloodGroup == BloodGroup.O:
            return True
        if recipient.bloodGroup == BloodGroup.AB:
            return True
        return recipient.bloodGroup == self.bloodGroup

    def addTransplant(self, transplant: "Transplant") -> None:
        """Add a potential transplant from this donor.

        :param transplant: the transplant object
        """
        self._outgoingTransplants.append(transplant)

    def transplants(self) -> list[Transplant]:
        """Return the list of transplants associated with this Donor.

        :return: A list of transplants
        """
        return self._outgoingTransplants


class Transplant:
    """A potential transplant."""

    def __init__(self, donor: Donor, recipient: Recipient, weight: float):
        self._donor: Donor = donor
        self._recipient: Recipient = recipient
        self._weight: float = weight

    def __str__(self):
        """Return a string representation of this transplant."""
        return f"Transplant({self.donor.id},{self.recipient.id},{self.weight})"

    @property
    def donor(self) -> Donor:
        return self._donor

    @property
    def recipient(self) -> Recipient:
        return self._recipient

    @property
    def weight(self) -> float:
        return self._weight


class Instance:
    """A KEP instance."""

    def __init__(self) -> None:
        """Create a new KEP instance."""
        self._donors: dict[str, Donor] = {}
        self._recips: dict[str, Recipient] = {}
        self._transplants: list[Transplant] = []

    def addDonor(self, donor: Donor) -> None:
        """Add a donor to the instance.

        :param donor: The Donor being added
        """
        if donor.id in self._donors:
            raise KEPDataValidationException(
                f"Trying to replace Donor {donor.id} in instance"
            )
        self._donors[donor.id] = donor

    def recipient(self, id: str, create: bool = True) -> Recipient:
        """Get a recipient from the instance by ID. If the recipient
        does not exist, create one with no details.

        :param id: the ID of the recipient
        :param create: If True, will create recipient if it doesn't
            exist. If False, and the recipient does not exist, will
            raise an exception.
        :return: the recipient
        """
        if id in self._recips:
            return self._recips[id]
        if not create:
            raise KEPDataValidationException(f"Recipient with ID '{id}' not found")
        recip = Recipient(id)
        self._recips[id] = recip
        return recip

    def recipients(self) -> ValuesView[Recipient]:
        """Return a list of all recipients.

        :return: a list of recipients
        """
        return self._recips.values()

    def addTransplant(self, transplant: Transplant) -> None:
        """Add a potential transplant to this instance.

        :param transplant: The transplant
        """
        self._transplants.append(transplant)
        transplant.donor.addTransplant(transplant)

    def donors(self) -> ValuesView[Donor]:
        """Return a generator object that can iterate through donors
        in a list-like fashion. Note that this list cannot itself be
        modified.

        :return: a list of donors
        """
        return self._donors.values()

    def donor(self, id: str) -> Donor:
        """Return a donor by ID:

        :param id: a donor ID
        :return: the donor
        """
        return self._donors[id]

    def transplants(self) -> list[Transplant]:
        return self._transplants
