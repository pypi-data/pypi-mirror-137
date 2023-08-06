# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# Copyright 2021 Daniel Mark Gass, see __about__.py for license information.
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
"""Test items transform API conformance."""

from baseline import Baseline

from plum.bigendian import uint8
from plum.conformance import Case, CaseData
from plum.items import ItemsX


class Test(Case):

    """Test items transform API conformance."""

    data = CaseData(
        fmt=ItemsX("items", fmt=({"a": uint8}, [uint8], uint8)),
        bindata=b"\x01\x02\x03",
        nbytes=3,
        values=(
            ({"a": 1}, [2], 3),  # tuple/list matches fmt
            [{"a": 1}, (2,), 3],  # tuple/list opposite fmt
        ),
        dump=Baseline(
            """
            +--------+---------+-------+-------+--------+
            | Offset | Access  | Value | Bytes | Format |
            +--------+---------+-------+-------+--------+
            |        |         |       |       | items  |
            |        | [0]     |       |       |        |
            | 0      |   ['a'] | 1     | 01    | uint8  |
            |        | [1]     |       |       |        |
            | 1      |   [0]   | 2     | 02    | uint8  |
            | 2      | [2]     | 3     | 03    | uint8  |
            +--------+---------+-------+-------+--------+
            """
        ),
        excess=Baseline(
            """
            +--------+---------+----------------+-------+--------+
            | Offset | Access  | Value          | Bytes | Format |
            +--------+---------+----------------+-------+--------+
            |        |         |                |       | items  |
            |        | [0]     |                |       |        |
            | 0      |   ['a'] | 1              | 01    | uint8  |
            |        | [1]     |                |       |        |
            | 1      |   [0]   | 2              | 02    | uint8  |
            | 2      | [2]     | 3              | 03    | uint8  |
            +--------+---------+----------------+-------+--------+
            | 3      |         | <excess bytes> | 99    |        |
            +--------+---------+----------------+-------+--------+

            ExcessMemoryError occurred during unpack operation:

            1 unconsumed bytes
            """
        ),
        shortage=Baseline(
            """
            +--------+---------+----------------------+-------+--------+
            | Offset | Access  | Value                | Bytes | Format |
            +--------+---------+----------------------+-------+--------+
            |        |         |                      |       | items  |
            |        | [0]     |                      |       |        |
            | 0      |   ['a'] | 1                    | 01    | uint8  |
            |        | [1]     |                      |       |        |
            | 1      |   [0]   | 2                    | 02    | uint8  |
            |        | [2]     | <insufficient bytes> |       | uint8  |
            +--------+---------+----------------------+-------+--------+

            InsufficientMemoryError occurred during unpack operation:

            1 too few bytes to unpack 'uint8' (1 needed, only 0 available)
            """
        ),
    )
