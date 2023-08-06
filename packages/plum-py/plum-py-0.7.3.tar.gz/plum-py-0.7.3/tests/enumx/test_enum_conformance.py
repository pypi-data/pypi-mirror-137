# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# Copyright 2021 Daniel Mark Gass, see __about__.py for license information.
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
"""Test integer enumeration transform API conformance."""

from baseline import Baseline

from plum.enum import EnumX
from plum.conformance import Case, CaseData

from sample_enum import Register


class TestConformance(Case):

    """Test integer enumeration transform conformance."""

    data = CaseData(
        fmt=EnumX("register16", Register, nbytes=2, byteorder="big", signed=False),
        bindata=b"\x00\x01",
        nbytes=2,
        values=(Register.SP, 1),
        dump=Baseline(
            """
            +--------+-------------+-------+------------+
            | Offset | Value       | Bytes | Format     |
            +--------+-------------+-------+------------+
            | 0      | Register.SP | 00 01 | register16 |
            +--------+-------------+-------+------------+
            """
        ),
        excess=Baseline(
            """
            +--------+----------------+-------+------------+
            | Offset | Value          | Bytes | Format     |
            +--------+----------------+-------+------------+
            | 0      | Register.SP    | 00 01 | register16 |
            +--------+----------------+-------+------------+
            | 2      | <excess bytes> | 99    |            |
            +--------+----------------+-------+------------+

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
