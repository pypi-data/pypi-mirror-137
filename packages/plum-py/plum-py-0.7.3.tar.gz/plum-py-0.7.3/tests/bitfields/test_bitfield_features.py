# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# Copyright 2021 Daniel Mark Gass, see __about__.py for license information.
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
"""Test basic features of BitField member class."""

import pytest
from baseline import Baseline

from plum.bitfields import BitFields, bitfield
from plum.conformance import wrap_message

from sample_bitfields import MyBits


class TestFeatures:

    """Test misc. features."""

    def test_repr(self):
        expected = Baseline(
            """
            BitField(name='bitfield')
            """
        )

        bitfield_ = bitfield(lsb=0, size=1)
        bitfield_.finish_initialization("bitfield")

        assert repr(bitfield_) == expected

    def test_default_type(self):
        # no arg, no annotation
        bitfield_ = bitfield(lsb=0, size=1)
        bitfield_.finish_initialization("bitfield")
        assert bitfield_.typ is int


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
            bitfield(lsb=-1, size=2, signed=True)

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
            bitfield(typ=1, lsb=0, size=2, signed=True)

        assert wrap_message(trap.value) == expected

    def test_invalid_class(self):
        """Test typ is not int-like."""

        expected = Baseline(
            """
            bit field type must be int-like
            """
        )

        with pytest.raises(TypeError) as trap:
            bitfield(typ=float, lsb=0, size=2, signed=True)

        assert wrap_message(trap.value) == expected

    def test_not_marked_nested(self):
        """Test typ as a BitFields but wasn't set up to support nested."""

        expected = Baseline(
            """
            bit field typ must be declared as nested (e.g. 'class
            MyBits(BitFields, nested=True):')
            """
        )

        with pytest.raises(TypeError) as trap:
            bitfield(size=2, typ=MyBits)

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

            class MyBitFields(BitFields):  # pylint: disable=unused-variable
                f1 = bitfield(lsb=0, size=2, signed=True, typ=1)

        assert wrap_message(trap.value) == expected

    def test_invalid_class(self):
        """Test typ is not int-like."""

        expected = Baseline(
            """
            bit field type must be int-like
            """
        )

        with pytest.raises(TypeError) as trap:

            class MyBitFields(BitFields):  # pylint: disable=unused-variable
                f1 = bitfield(lsb=0, size=2, signed=True, typ=float)

        assert wrap_message(trap.value) == expected


class TestInvalidSizes:

    """Test invalid bit sizes for bit field member."""

    def test_signed_int(self):
        """Test bit size restriction for signed int."""

        # no exception
        bitfield(lsb=0, size=2, signed=True)

        expected = Baseline(
            """
            'size' must be 2 or greater for signed bit field
            """
        )

        with pytest.raises(ValueError) as trap:
            bitfield(lsb=0, size=1, signed=True)
        assert wrap_message(trap.value) == expected

        with pytest.raises(ValueError) as trap:
            bitfield(lsb=0, size=0, signed=True)
        assert wrap_message(trap.value) == expected

        with pytest.raises(ValueError) as trap:
            bitfield(lsb=0, size=-1, signed=True)
        assert wrap_message(trap.value) == expected

    def test_unsigned_int(self):
        """Test bit size restriction for unsigned int."""

        # no exception
        bitfield(lsb=0, size=1, signed=False)

        expected = Baseline(
            """
            'size' must be 1 or greater for unsigned bit field
            """
        )

        with pytest.raises(ValueError) as trap:
            bitfield(lsb=0, size=0, signed=False)
        assert wrap_message(trap.value) == expected

        with pytest.raises(ValueError) as trap:
            bitfield(lsb=0, size=-1, signed=False)
        assert wrap_message(trap.value) == expected


class TestInvalidDefault:

    """Test out of range default for bit field member."""

    def test_too_small(self):
        expected = Baseline(
            """
            bit field requires 0 <= default <= 3
            """
        )

        with pytest.raises(ValueError) as trap:
            bitfield(size=2, default=-1)
        assert wrap_message(trap.value) == expected

    def test_too_big(self):
        expected = Baseline(
            """
            bit field requires 0 <= default <= 3
            """
        )

        with pytest.raises(ValueError) as trap:
            bitfield(size=2, default=4)
        assert wrap_message(trap.value) == expected
