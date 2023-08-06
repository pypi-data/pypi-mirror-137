# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# Copyright 2021 Daniel Mark Gass, see __about__.py for license information.
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
"""Test basic features of bitfield_member() definition."""

import pytest
from baseline import Baseline

from plum.conformance import wrap_message
from plum.structure import Structure, bitfield_member


class TestMiscFeatures:

    """Test misc. features."""

    class Struct(Structure):
        f1 = bitfield_member(size=1)

    def test_repr(self):

        expected = Baseline(
            """
            BitFieldMember(name='f1')
            """
        )

        assert repr(self.Struct.f1) == expected

    def test_default_type(self):
        # no arg, no annotation
        assert self.Struct.f1.typ is int


class TestInvalidPosition:

    """Test invalid bit position for bit field member."""

    def test_less_than_zero(self):
        """Test bit position less than zero."""

        expected = Baseline(
            """
            bit field position must be greater than or equal to zero
            """
        )

        with pytest.raises(TypeError) as trap:
            bitfield_member(lsb=-1, size=2, signed=True)

        assert wrap_message(trap.value) == expected


class TestInvalidTypExplicit:

    """Test invalid bit field typ when specified incorrectly in member."""

    def test_instance(self):
        """Test typ is not a class but an instance of a class."""

        expected = Baseline(
            """
            bit field type must be int-like
            """
        )

        with pytest.raises(TypeError) as trap:
            bitfield_member(typ=1, lsb=0, size=2, signed=True)

        assert wrap_message(trap.value) == expected

    def test_invalid_class(self):
        """Test typ is not int-like."""

        expected = Baseline(
            """
            bit field type must be int-like
            """
        )

        with pytest.raises(TypeError) as trap:
            bitfield_member(typ=float, lsb=0, size=2, signed=True)

        assert wrap_message(trap.value) == expected


class TestInvalidTypAnnotation:

    """Test invalid bit field typ when specified via annotation."""

    def test_instance(self):
        """Test typ is not a class but an instance of a class."""
        expected = Baseline(
            """
            bit field type must be int-like
            """
        )

        with pytest.raises(TypeError) as trap:

            class Struct(Structure):  # pylint: disable=unused-variable
                f1 = bitfield_member(lsb=0, size=2, signed=True, typ=1)

        assert wrap_message(trap.value) == expected

    def test_invalid_class(self):
        """Test typ is not int-like."""
        expected = Baseline(
            """
            bit field type must be int-like
            """
        )

        with pytest.raises(TypeError) as trap:

            class Struct(Structure):  # pylint: disable=unused-variable
                f1 = bitfield_member(lsb=0, size=2, signed=True, typ=float)

        assert wrap_message(trap.value) == expected


class TestInvalidSizes:

    """Test invalid bit sizes for bit field member."""

    def test_signed_int(self):
        """Test bit size restriction for signed int."""

        # no exception
        bitfield_member(lsb=0, size=2, signed=True)

        expected = Baseline(
            """
            'size' must be 2 or greater for signed bit field
            """
        )

        with pytest.raises(ValueError) as trap:
            bitfield_member(lsb=0, size=1, signed=True)
        assert wrap_message(trap.value) == expected

        with pytest.raises(ValueError) as trap:
            bitfield_member(lsb=0, size=0, signed=True)
        assert wrap_message(trap.value) == expected

        with pytest.raises(ValueError) as trap:
            bitfield_member(lsb=0, size=-1, signed=True)
        assert wrap_message(trap.value) == expected

    def test_unsigned_int(self):
        """Test bit size restriction for unsigned int."""

        # no exception
        bitfield_member(lsb=0, size=1, signed=False)

        expected = Baseline(
            """
            'size' must be 1 or greater for unsigned bit field
            """
        )

        with pytest.raises(ValueError) as trap:
            bitfield_member(lsb=0, size=0, signed=False)
        assert wrap_message(trap.value) == expected

        with pytest.raises(ValueError) as trap:
            bitfield_member(lsb=0, size=-1, signed=False)
        assert wrap_message(trap.value) == expected


class TestInvalidInitValues:

    """Test out of range values passed to constructor."""

    class Struct(Structure):
        f1 = bitfield_member(size=4, default=0)
        f2 = bitfield_member(size=4, signed=True, default=0)

    unsigned_message = Baseline(
        """
        'f1' out of range, 0 <= f1 <= 15
        """
    )

    signed_message = Baseline(
        """
        'f2' out of range, -8 <= f2 <= 7
        """
    )

    def test_too_small_for_signed(self):
        with pytest.raises(ValueError) as trap:
            self.Struct(f2=-9)

        assert wrap_message(trap.value) == self.signed_message

    def test_too_small_for_unsigned(self):
        with pytest.raises(ValueError) as trap:
            self.Struct(f1=-1)

        assert wrap_message(trap.value) == self.unsigned_message

    def test_too_big_for_signed(self):
        with pytest.raises(ValueError) as trap:
            self.Struct(f2=8)

        assert wrap_message(trap.value) == self.signed_message

    def test_too_big_for_unsigned(self):
        with pytest.raises(ValueError) as trap:
            self.Struct(f1=16)

        assert wrap_message(trap.value) == self.unsigned_message


class TestInvalidAttributeValues:

    """Test out of range attribute values."""

    class Struct(Structure):
        f1 = bitfield_member(size=4, default=0)
        f2 = bitfield_member(size=4, signed=True, default=0)

    unsigned_message = Baseline(
        """
        out of range, 0 <= value <= 15
        """
    )

    signed_message = Baseline(
        """
        out of range, -8 <= value <= 7
        """
    )

    def test_too_small_for_signed(self):
        with pytest.raises(ValueError) as trap:
            self.Struct().f2 = -9  # pylint: disable=invalid-name

        assert wrap_message(trap.value) == self.signed_message

    def test_too_small_for_unsigned(self):
        with pytest.raises(ValueError) as trap:
            self.Struct().f1 = -1  # pylint: disable=invalid-name

        assert wrap_message(trap.value) == self.unsigned_message

    def test_too_big_for_signed(self):
        with pytest.raises(ValueError) as trap:
            self.Struct().f2 = 8

        assert wrap_message(trap.value) == self.signed_message

    def test_too_big_for_unsigned(self):
        with pytest.raises(ValueError) as trap:
            self.Struct().f1 = 16

        assert wrap_message(trap.value) == self.unsigned_message


class TestDefaultFactory:
    class Struct(Structure):
        def get_default(self):
            return self.f1 * 2

        f1 = bitfield_member(size=4)
        f2 = bitfield_member(size=4, default=get_default)

    def test_factory(self):
        assert self.Struct(f1=1).f2 == 2
