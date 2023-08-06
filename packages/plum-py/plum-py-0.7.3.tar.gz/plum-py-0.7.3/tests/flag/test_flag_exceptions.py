# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# Copyright 2021 Daniel Mark Gass, see __about__.py for license information.
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
"""Test integer flag enumeration transform exceptions."""

import pytest
from baseline import Baseline

from plum.conformance import wrap_message
from plum.exceptions import PackError
from plum.flag import FlagX

from sample_flag import Register


register16 = FlagX("register16", Register, byteorder="little", nbytes=2)


class TestPack:

    """Test pack exceptions."""

    def test_not_int_val(self):
        """Test not integer values."""
        with pytest.raises(PackError) as trap:
            register16.pack("str")

        expected = Baseline(
            """
            +--------+-------+-------+------------+
            | Offset | Value | Bytes | Format     |
            +--------+-------+-------+------------+
            |        | 'str' |       | register16 |
            +--------+-------+-------+------------+

            ValueError occurred during pack operation:

            invalid literal for int() with base 10: 'str'
            """
        )

        assert wrap_message(trap.value) == expected
