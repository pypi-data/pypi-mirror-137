# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# Copyright 2021 Daniel Mark Gass, see __about__.py for license information.
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
"""Test construction of bit field classes."""

# pylint: disable=invalid-name

import pytest
from baseline import Baseline

from plum.structure import Structure, bitfield_member
from plum.conformance import wrap_message


class TestExceptions:

    """Test validation of class."""

    @staticmethod
    def test_bitfield_bad_type():
        """Test annotation contains bad type."""

        expected_message = Baseline(
            """
            bit field type must be int-like
            """
        )

        with pytest.raises(TypeError) as trap:

            class Sample(Structure):  # pylint: disable=unused-variable

                f1: int = bitfield_member(lsb=0, size=8)
                f2 = bitfield_member(lsb=8, size=8, typ=str)

        assert wrap_message(trap.value) == expected_message

    @staticmethod
    def test_bitfield_overlap():
        """Test bit fields overlap."""

        expected_message = Baseline(
            """
            bit field 'f2' overlaps with 'f1'
            """
        )

        with pytest.raises(TypeError) as trap:

            class Sample(Structure):  # pylint: disable=unused-variable

                f1: int = bitfield_member(lsb=0, size=8)
                f2: int = bitfield_member(lsb=7, size=8)

        assert wrap_message(trap.value) == expected_message

    @staticmethod
    def test_nbytes_too_small():
        """Test nbytes argument insufficient size."""

        expected_message = Baseline(
            """
            'nbytes' must be at least 2 for bitfield 'f1' (to have sufficient room
            for it and those that follow)
            """
        )

        with pytest.raises(TypeError) as trap:

            class Sample(Structure):  # pylint: disable=unused-variable

                f1: int = bitfield_member(lsb=0, size=8, nbytes=1)
                f2: int = bitfield_member(lsb=8, size=8)

        assert wrap_message(trap.value) == expected_message
