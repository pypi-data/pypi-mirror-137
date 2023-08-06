# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# Copyright 2021 Daniel Mark Gass, see __about__.py for license information.
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
"""Test common exceptions using BitFields data store transform."""

import pytest
from baseline import Baseline

from plum.bitfields import BitFields, bitfield
from plum.conformance import wrap_message

from sample_bitfields import MyBits


class TestExceptions:
    def test_attribute_fat_finger(self):
        """Test invalid attribute set."""
        expected_message = Baseline(
            """
            'MyBits' has no attribute 'junk'
            """
        )

        mybits = MyBits.from_int(0)

        with pytest.raises(AttributeError) as trap:
            # pylint: disable=attribute-defined-outside-init
            mybits.junk = 1

        assert wrap_message(trap.value) == expected_message

    def test_already_in_use(self):
        """Test bit field definition may only be used in one BitsField class."""

        expected = Baseline(
            """
            invalid bit field 'xyz' definition, BitField() instance can not be
            shared between bit fields classes
            """
        )

        bitfield_ = bitfield(typ=int, lsb=0, size=1)

        class FirstUse(BitFields, nbytes=1):  # pylint: disable=unused-variable

            """Sample bit fields."""

            xyz = bitfield_

        with pytest.raises(TypeError) as trap:

            class SecondUse(BitFields, nbytes=1):  # pylint: disable=unused-variable
                """Sample bit fields."""

                xyz = bitfield_

        assert wrap_message(trap.value) == expected

    def test_from_int_too_small(self):
        expected_message = Baseline(
            """
            MyBits.from_int() requires 0 <= value <= 65535
            """
        )

        with pytest.raises(ValueError) as trap:
            MyBits.from_int(-1)

        assert wrap_message(trap.value) == expected_message

    def test_from_int_too_big(self):
        expected_message = Baseline(
            """
            MyBits.from_int() requires 0 <= value <= 65535
            """
        )

        with pytest.raises(ValueError) as trap:
            MyBits.from_int(0x10000)

        assert wrap_message(trap.value) == expected_message
