# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# Copyright 2021 Daniel Mark Gass, see __about__.py for license information.
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
"""Test integer flag enumeration transform API conformance."""

from baseline import Baseline

from plum.conformance import Case, CaseData
from plum.flag import FlagX

from sample_flag import Register


register16 = FlagX("register16", Register, byteorder="big", nbytes=2)


class TestConformance(Case):

    """Test integer flag enumeration transform conformance."""

    data = CaseData(
        fmt=register16,
        bindata=b"\x00\x01",
        nbytes=2,
        values=(Register.SP, 1),
        dump=Baseline(
            """
            +--------+--------+-------+-------------------+------------+
            | Offset | Access | Value | Bytes             | Format     |
            +--------+--------+-------+-------------------+------------+
            | 0      |        | 1     | 00 01             | register16 |
            |  [0]   | .sp    | True  | ........ .......1 | bool       |
            |  [1]   | .r0    | False | ........ ......0. | bool       |
            |  [2]   | .r1    | False | ........ .....0.. | bool       |
            +--------+--------+-------+-------------------+------------+
            """
        ),
        excess=Baseline(
            """
            +--------+--------+----------------+-------------------+------------+
            | Offset | Access | Value          | Bytes             | Format     |
            +--------+--------+----------------+-------------------+------------+
            | 0      |        | 1              | 00 01             | register16 |
            |  [0]   | .sp    | True           | ........ .......1 | bool       |
            |  [1]   | .r0    | False          | ........ ......0. | bool       |
            |  [2]   | .r1    | False          | ........ .....0.. | bool       |
            +--------+--------+----------------+-------------------+------------+
            | 2      |        | <excess bytes> | 99                |            |
            +--------+--------+----------------+-------------------+------------+

            ExcessMemoryError occurred during unpack operation:

            1 unconsumed bytes
            """
        ),
        shortage=Baseline(
            """
            +--------+----------------------+-------+------------+
            | Offset | Value                | Bytes | Format     |
            +--------+----------------------+-------+------------+
            | 0      | <insufficient bytes> | 00    | register16 |
            +--------+----------------------+-------+------------+

            InsufficientMemoryError occurred during unpack operation:

            1 too few bytes to unpack 'register16' (2 needed, only 1 available)
            """
        ),
    )
