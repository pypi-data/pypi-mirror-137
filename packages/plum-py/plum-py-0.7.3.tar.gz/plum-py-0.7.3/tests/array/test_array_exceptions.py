# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# Copyright 2021 Daniel Mark Gass, see __about__.py for license information.
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
"""Test exception corner cases with Array type usage."""

import pytest
from baseline import Baseline

from plum.array import ArrayX
from plum.bigendian import uint8
from plum.conformance import wrap_message
from plum.exceptions import PackError, UnpackError
from plum.utilities import pack, unpack


class TestUnpack:

    """Test exception cases during unpack."""

    def test_greedy_multidimensional(self):
        """Verify exception/message when None specified for one of the dimensions."""

        # sample array type with second dimension unspecified
        customarray = ArrayX("customarray", fmt=uint8, dims=(2, None))

        with pytest.raises(UnpackError) as trap:
            unpack(customarray, bytes(10))

        expected = Baseline(
            """
            +--------+-------+-------+-------------+
            | Offset | Value | Bytes | Format      |
            +--------+-------+-------+-------------+
            |        |       |       | customarray |
            +--------+-------+-------+-------------+

            TypeError occurred during unpack operation:

            array unpack does not support greedy secondary dimensions
            """
        )

        assert wrap_message(trap.value) == expected


class TestPack:

    """Test exception cases during pack."""

    def test_greedy_noniterable(self):
        """Pack non-iterable value with greedy array."""

        array = ArrayX("array", fmt=uint8)

        with pytest.raises(PackError) as trap:
            pack(0, array)

        expected = Baseline(
            """
            +--------+-------+-------+--------+
            | Offset | Value | Bytes | Format |
            +--------+-------+-------+--------+
            |        | 0     |       | array  |
            +--------+-------+-------+--------+

            TypeError occurred during pack operation:

            invalid value, expected iterable of any length, got non-iterable
            """
        )

        assert wrap_message(trap.value) == expected

    def test_dimensioned_noniterable(self):
        """Pack non-iterable value with fixed dimension array."""
        customarray = ArrayX("customarray", fmt=uint8, dims=(2,))

        with pytest.raises(PackError) as trap:
            pack(0, customarray)

        expected = Baseline(
            """
            +--------+-------+-------+-------------+
            | Offset | Value | Bytes | Format      |
            +--------+-------+-------+-------------+
            |        | 0     |       | customarray |
            +--------+-------+-------+-------------+

            TypeError occurred during pack operation:

            invalid value, expected iterable of length 2, got non-iterable
            """
        )

        assert wrap_message(trap.value) == expected

    def test_dimension_mismatch_missing(self):
        """Pack iterable value but length does not match array fixed dimension (missing)."""
        customarray = ArrayX("customarray", fmt=uint8, dims=(2,))

        with pytest.raises(PackError) as trap:
            pack([1], customarray)

        expected = Baseline(
            """
            +--------+--------+-----------+-------+-------------+
            | Offset | Access | Value     | Bytes | Format      |
            +--------+--------+-----------+-------+-------------+
            |        |        |           |       | customarray |
            | 0      | [0]    | 1         | 01    | uint8       |
            |        | [1]    | <missing> |       |             |
            +--------+--------+-----------+-------+-------------+

            TypeError occurred during pack operation:

            invalid value, expected iterable of 2 length, got iterable of length 1
            """
        )

        assert wrap_message(trap.value) == expected

    def test_dimension_mismatch_extra(self):
        """Pack iterable value but length does not match array fixed dimension (extra)."""
        customarray = ArrayX("customarray", fmt=uint8, dims=(2,))

        with pytest.raises(PackError) as trap:
            pack([1, 2, 3], customarray)

        expected = Baseline(
            """
            +--------+-------------+-------+-------+-------------+
            | Offset | Access      | Value | Bytes | Format      |
            +--------+-------------+-------+-------+-------------+
            |        |             |       |       | customarray |
            | 0      | [0]         | 1     | 01    | uint8       |
            | 1      | [1]         | 2     | 02    | uint8       |
            +--------+-------------+-------+-------+-------------+
            |        | [2] <extra> | 3     |       |             |
            +--------+-------------+-------+-------+-------------+

            TypeError occurred during pack operation:

            invalid value, expected iterable of 2 length, got iterable of length 3
            """
        )

        assert wrap_message(trap.value) == expected
