# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# Copyright 2021 Daniel Mark Gass, see __about__.py for license information.
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
"""Test float transform properties."""

from plum.float import FloatX


class TestDefault:

    """Test with as many left to default as possible."""

    float32 = FloatX("float32", nbytes=4)

    def test_name(self):
        assert self.float32.name == "float32"

    def test_nbytes(self):
        assert self.float32.nbytes == 4

    def test_byteorder(self):
        assert self.float32.byteorder == "little"


class TestPositional:

    """Test explicitly defined with positional argument."""

    float32 = FloatX("float32", 4, "big")

    def test_name(self):
        assert self.float32.name == "float32"

    def test_nbytes(self):
        assert self.float32.nbytes == 4

    def test_byteorder(self):
        assert self.float32.byteorder == "big"


class TestKeyword(TestPositional):

    """Test explicitly defined with keyword argument."""

    float32 = FloatX(name="float32", nbytes=4, byteorder="big")
