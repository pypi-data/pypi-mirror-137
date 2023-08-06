# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# Copyright 2021 Daniel Mark Gass, see __about__.py for license information.
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
"""Test integer transform properties."""

from plum.int import IntX


class TestDefault:

    """Test with as many left to default as possible."""

    uint8 = IntX("uint8", 1)

    def test_name(self):
        assert self.uint8.name == "uint8"

    def test_nbytes(self):
        assert self.uint8.nbytes == 1

    def test_byteorder(self):
        assert self.uint8.byteorder == "little"

    def test_signed(self):
        assert self.uint8.signed is False


class TestPositional:

    """Test explicitly defined with positional argument."""

    uint8 = IntX("uint8", 2, "big", signed=True)

    def test_name(self):
        assert self.uint8.name == "uint8"

    def test_nbytes(self):
        assert self.uint8.nbytes == 2

    def test_byteorder(self):
        assert self.uint8.byteorder == "big"

    def test_signed(self):
        assert self.uint8.signed is True


class TestKeyword(TestPositional):

    """Test explicitly defined with keyword argument."""

    uint8 = IntX(name="uint8", nbytes=2, byteorder="big", signed=True)
