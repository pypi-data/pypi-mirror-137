# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# Copyright 2021 Daniel Mark Gass, see __about__.py for license information.
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
"""Test get/set item (indexing) BitFields data store transform."""

import pytest
from baseline import Baseline

from plum.bitfields import BitFields
from plum.conformance import wrap_message


class Sample(BitFields, nbytes=1):

    """No bit fields."""


class TestHappyPath:
    def test_get(self):
        sample = Sample.from_int(0xAB)
        assert sample[:] == [True, True, False, True, False, True, False, True]
        assert sample[0] is True
        assert sample[2] is False
        assert sample[7] is True

    def test_set_single_with_bool(self):
        sample = Sample.from_int(0)
        sample[0] = True
        assert int(sample) == 1

    def test_reset_single_with_bool(self):
        sample = Sample.from_int(0xFF)
        sample[0] = False
        assert int(sample) == 0xFE

    def test_set_range(self):
        sample = Sample.from_int(0)
        sample[1:5] = [True, False, True, True]
        assert int(sample) == 0x1A

    def test_reset_range(self):
        sample = Sample.from_int(255)
        sample[1:5] = [False, True, False, False]
        assert int(sample) == 0xE5


class TestExceptions:
    def test_wrong_slice_size(self):
        expected_massage = Baseline(
            """
            slice and value not same length
            """
        )
        sample = Sample.from_int(0)
        with pytest.raises(ValueError) as trap:
            sample[0:1] = [True, True]

        assert wrap_message(trap.value) == expected_massage
