# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# Copyright 2021 Daniel Mark Gass, see __about__.py for license information.
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
"""Test integer transform exceptions."""

# pylint: disable=unidiomatic-typecheck

import pytest

from baseline import Baseline

from plum.bigendian import uint8
from plum.conformance import wrap_message
from plum.exceptions import PackError
from plum.utilities import pack


class TestPack:

    """Test pack transform exceptions."""

    def test_not_int_val(self):
        """Test not integer values."""
        with pytest.raises(PackError) as trap:
            pack("str", uint8)

        expected = Baseline(
            """
            +--------+-------+-------+--------+
            | Offset | Value | Bytes | Format |
            +--------+-------+-------+--------+
            |        | 'str' |       | uint8  |
            +--------+-------+-------+--------+

            TypeError occurred during pack operation:

            value type <class 'str'> not int-like (no to_bytes() method)
            """
        )

        assert wrap_message(trap.value) == expected

    def test_less_than_minimum(self):
        """Test value too little."""
        with pytest.raises(PackError) as trap:
            pack(-1, uint8)

        expected_context = Baseline(
            """
            can't convert negative int to unsigned
            """
        )

        expected = Baseline(
            """
            +--------+-------+-------+--------+
            | Offset | Value | Bytes | Format |
            +--------+-------+-------+--------+
            |        | -1    |       | uint8  |
            +--------+-------+-------+--------+

            OverflowError occurred during pack operation:

            can't convert negative int to unsigned
            """
        )

        context_message_match = wrap_message(trap.value.__context__) == expected_context
        message_match = wrap_message(trap.value) == expected
        assert context_message_match and message_match
        assert type(trap.value.__context__) is OverflowError

    def test_exceeds_maximum(self):
        """Test value too large."""
        with pytest.raises(PackError) as trap:
            pack(256, uint8)

        expected_context = Baseline(
            """
            int too big to convert
            """
        )

        expected = Baseline(
            """
            +--------+-------+-------+--------+
            | Offset | Value | Bytes | Format |
            +--------+-------+-------+--------+
            |        | 256   |       | uint8  |
            +--------+-------+-------+--------+

            OverflowError occurred during pack operation:

            int too big to convert
            """
        )

        context_message_match = wrap_message(trap.value.__context__) == expected_context
        message_match = wrap_message(trap.value) == expected
        assert context_message_match and message_match
        assert type(trap.value.__context__) is OverflowError
