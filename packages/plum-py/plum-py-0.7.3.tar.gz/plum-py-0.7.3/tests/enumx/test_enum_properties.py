# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# Copyright 2021 Daniel Mark Gass, see __about__.py for license information.
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
"""Test integer enumeration transform properties."""

from plum.enum import EnumX

from sample_enum import Register


class TestDefault:

    """Test with as many left to default as possible."""

    register = EnumX("register", Register)

    def test_name(self):
        assert self.register.name == "register"

    def test_enum(self):
        assert self.register.enum is Register

    def test_nbytes(self):
        assert self.register.nbytes == 1

    def test_byteorder(self):
        assert self.register.byteorder == "little"

    def test_signed(self):
        assert self.register.signed is False

    def test_strict(self):
        assert self.register.strict is True


class TestPositional:

    """Test explicitly defined with positional argument."""

    register = EnumX("register", Register, 2, "big", signed=True, strict=False)

    def test_name(self):
        assert self.register.name == "register"

    def test_enum(self):
        assert self.register.enum is Register

    def test_nbytes(self):
        assert self.register.nbytes == 2

    def test_byteorder(self):
        assert self.register.byteorder == "big"

    def test_signed(self):
        assert self.register.signed is True

    def test_strict(self):
        assert self.register.strict is False


class TestKeyword(TestPositional):

    """Test explicitly defined with keyword argument."""

    register = EnumX(
        name="register",
        enum=Register,
        nbytes=2,
        byteorder="big",
        signed=True,
        strict=False,
    )
