# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# Copyright 2021 Daniel Mark Gass, see __about__.py for license information.
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
"""Test integer enumeration transform properties."""

from plum.flag import FlagX

from sample_flag import Register


class TestDefault:

    """Test with as many left to default as possible."""

    register = FlagX("register", Register, 1)

    def test_name(self):
        assert self.register.name == "register"

    def test_enum(self):
        assert self.register.enum is Register

    def test_nbytes(self):
        assert self.register.nbytes == 1

    def test_byteorder(self):
        assert self.register.byteorder == "little"


class TestPositional:

    """Test explicitly defined with positional argument."""

    register = FlagX("register", Register, 2, "big")

    def test_name(self):
        assert self.register.name == "register"

    def test_enum(self):
        assert self.register.enum is Register

    def test_nbytes(self):
        assert self.register.nbytes == 2

    def test_byteorder(self):
        assert self.register.byteorder == "big"


class TestKeyword(TestPositional):

    """Test explicitly defined with keyword argument."""

    register = FlagX(name="register", enum=Register, nbytes=2, byteorder="big")
