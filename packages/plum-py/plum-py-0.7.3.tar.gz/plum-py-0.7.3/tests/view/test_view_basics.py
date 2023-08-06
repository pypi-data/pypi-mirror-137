# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# Copyright 2021 Daniel Mark Gass, see __about__.py for license information.
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
"""Test base view basic methods and behaviors."""

from plum.int import IntX
from plum.structure import Structure, member

uint8 = IntX("uint8", nbytes=1)
uint16 = IntX("uint16", nbytes=2)


class SampleStruct(Structure):

    """Sample structure."""

    m1: int = member(fmt=uint8)


class TestCast:

    """Test base view cast() method."""

    def test_cast(self):
        """Test base view cast() method."""
        buffer = bytearray([0, 1, 2, 3])
        view_16 = uint16.view(buffer, offset=1)
        view_8 = view_16.cast(uint8)
        assert view_8 == 0x1
        assert view_16 == 0x0201
        view_8.set(0x99)
        assert view_8 == 0x99
        assert view_16 == 0x0299


class TestStr:

    """Test base view __str__() method."""

    def test_get_success(self):
        """Test str() conversion produces str() of datatype get()."""
        buffer = bytearray([0, 1, 2])
        view_8 = uint8.view(buffer, offset=1)
        assert str(view_8) == "1"

    def test_get_fail(self):
        """Test str() conversion produces representation when get() fails."""
        buffer = bytearray([0, 1, 2])
        view_8 = uint8.view(buffer, offset=3)
        assert str(view_8) == "<view at 0x3>"


class TestRepr:

    """Test base view __repr__() method."""

    def test_get_success(self):
        """Test repr() produces representation with value when get() successful."""
        buffer = bytearray([0, 1, 2])
        view_8 = uint8.view(buffer, offset=1)
        assert repr(view_8) == "<view at 0x1: uint8(1)>"

    def test_get_fail_number(self):
        """Test repr() produces representation without value when get() fails.

        Test number method.

        """
        buffer = bytearray([0, 1, 2])
        view_8 = uint8.view(buffer, offset=3)
        assert repr(view_8) == "<view at 0x3>"

    def test_get_fail_base(self):
        """Test repr() produces representation without value when get() fails.

        Test base View class method.
        """
        buffer = bytearray([0, 1, 2])
        view_8 = SampleStruct.view(buffer, offset=3)
        assert repr(view_8) == "<view at 0x3>"


class TestProperties:

    """Test base view properties."""

    def test_nbytes(self):
        assert SampleStruct.view(b"\x00").nbytes == 1
