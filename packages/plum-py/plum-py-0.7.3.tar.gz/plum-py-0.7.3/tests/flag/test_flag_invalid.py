# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# Copyright 2021 Daniel Mark Gass, see __about__.py for license information.
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
"""Test integer flag enumeration behavior when value is not a member combination."""

from enum import IntFlag

from baseline import Baseline

from plum.conformance import Case, CaseData
from plum.flag import FlagX

from sample_flag import Register


register = FlagX("register", Register, byteorder="little", nbytes=2)


class TestInvalidValue(Case):

    """Test value is not a member combination."""

    data = CaseData(
        fmt=register,
        bindata=b"\x63\x00",
        nbytes=2,
        values=[Register(99), 99],
        dump=Baseline(
            """
            +--------+--------+-------+-------------------+----------+
            | Offset | Access | Value | Bytes             | Format   |
            +--------+--------+-------+-------------------+----------+
            | 0      |        | 99    | 63 00             | register |
            |  [0]   | .sp    | True  | ........ .......1 | bool     |
            |  [1]   | .r0    | True  | ........ ......1. | bool     |
            |  [2]   | .r1    | False | ........ .....0.. | bool     |
            +--------+--------+-------+-------------------+----------+
            """
        ),
        excess="N/A",
        shortage="N/A",
    )


class Flag(IntFlag):

    """No members."""


flag16 = FlagX("flag16", Flag, byteorder="little", nbytes=2)


class TestNoMember(Case):

    """Test flag type behavior with no members."""

    data = CaseData(
        fmt=flag16,
        bindata=b"\x11\x00",
        nbytes=2,
        values=[Flag(17), 17],
        dump=Baseline(
            """
            +--------+-------+-------+--------+
            | Offset | Value | Bytes | Format |
            +--------+-------+-------+--------+
            | 0      | 17    | 11 00 | flag16 |
            +--------+-------+-------+--------+
            """
        ),
        excess="N/A",
        shortage="N/A",
    )
