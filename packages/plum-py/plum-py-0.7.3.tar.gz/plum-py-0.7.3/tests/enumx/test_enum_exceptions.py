# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# Copyright 2021 Daniel Mark Gass, see __about__.py for license information.
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
"""Test integer enumeration classes from little endian byte order module."""

import pytest
from baseline import Baseline

from plum.conformance import wrap_message
from plum.enum import EnumX
from plum.exceptions import PackError
from plum.utilities import pack

from sample_enum import Register


register16 = EnumX("register16", Register, nbytes=2, byteorder="big", signed=False)


class TestPack:

    """Test pack exceptions."""

    def test_not_int_val(self):
        """Test not integer values."""
        with pytest.raises(PackError) as trap:
            pack("str", register16)

        expected = Baseline(
            """
            +--------+-------+-------+------------+
            | Offset | Value | Bytes | Format     |
            +--------+-------+-------+------------+
            |        | 'str' |       | register16 |
            +--------+-------+-------+------------+

            ValueError occurred during pack operation:

            'str' is not a valid Register
            """
        )

        assert wrap_message(trap.value) == expected
