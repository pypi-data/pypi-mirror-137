# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# Copyright 2021 Daniel Mark Gass, see __about__.py for license information.
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
"""Test float transform API conformance."""

from baseline import Baseline

from plum.conformance import Case, CaseData
from plum.float import FloatX

float32 = FloatX("float32", byteorder="big", nbytes=4)


class TestConformance(Case):

    """Test float transform conformance."""

    data = CaseData(
        fmt=float32,
        bindata=b"\x40\x20\x00\x00",
        nbytes=4,
        values=(2.5,),
        dump=Baseline(
            """
            +--------+-------+-------------+---------+
            | Offset | Value | Bytes       | Format  |
            +--------+-------+-------------+---------+
            | 0      | 2.5   | 40 20 00 00 | float32 |
            +--------+-------+-------------+---------+
            """
        ),
        excess=Baseline(
            """
            +--------+----------------+-------------+---------+
            | Offset | Value          | Bytes       | Format  |
            +--------+----------------+-------------+---------+
            | 0      | 2.5            | 40 20 00 00 | float32 |
            +--------+----------------+-------------+---------+
            | 4      | <excess bytes> | 99          |         |
            +--------+----------------+-------------+---------+

            ExcessMemoryError occurred during unpack operation:

            1 unconsumed bytes
            """
        ),
        shortage=Baseline(
            """
            +--------+----------------------+----------+---------+
            | Offset | Value                | Bytes    | Format  |
            +--------+----------------------+----------+---------+
            | 0      | <insufficient bytes> | 40 20 00 | float32 |
            +--------+----------------------+----------+---------+

            InsufficientMemoryError occurred during unpack operation:

            1 too few bytes to unpack 'float32' (4 needed, only 3 available)
            """
        ),
    )
