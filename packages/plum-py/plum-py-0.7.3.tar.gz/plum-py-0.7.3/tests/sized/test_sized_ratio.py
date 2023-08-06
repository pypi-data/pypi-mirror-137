# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# Copyright 2021 Daniel Mark Gass, see __about__.py for license information.
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
"""Test SizedX transform API conformance."""

from baseline import Baseline

from plum.conformance import Case, CaseData
from plum.littleendian import uint8
from plum.sized import SizedX
from plum.str import StrX


ascii_greedy = StrX("ascii", encoding="ascii")

sized_string = SizedX("sized_string", fmt=ascii_greedy, size_fmt=uint8, ratio=0.5)


class TestApi(Case):

    data = CaseData(
        fmt=sized_string,
        bindata=b"\x18Hello World!",
        nbytes=None,
        values=["Hello World!"],
        dump=Baseline(
            """
            +--------+----------+----------------+-------------------------------------+--------------+
            | Offset | Access   | Value          | Bytes                               | Format       |
            +--------+----------+----------------+-------------------------------------+--------------+
            |        |          |                |                                     | sized_string |
            |  0     | --size-- | 24             | 18                                  | uint8        |
            |        |          |                |                                     | ascii        |
            |  1     | [0:12]   | 'Hello World!' | 48 65 6c 6c 6f 20 57 6f 72 6c 64 21 |              |
            +--------+----------+----------------+-------------------------------------+--------------+
            """
        ),
        excess=Baseline(
            """
            +--------+----------+----------------+-------------------------------------+--------------+
            | Offset | Access   | Value          | Bytes                               | Format       |
            +--------+----------+----------------+-------------------------------------+--------------+
            |        |          |                |                                     | sized_string |
            |  0     | --size-- | 24             | 18                                  | uint8        |
            |        |          |                |                                     | ascii        |
            |  1     | [0:12]   | 'Hello World!' | 48 65 6c 6c 6f 20 57 6f 72 6c 64 21 |              |
            +--------+----------+----------------+-------------------------------------+--------------+
            | 13     |          | <excess bytes> | 99                                  |              |
            +--------+----------+----------------+-------------------------------------+--------------+

            ExcessMemoryError occurred during unpack operation:

            1 unconsumed bytes
            """
        ),
        shortage=Baseline(
            """
        +--------+----------+----------------------+----------------------------------+--------------+
        | Offset | Access   | Value                | Bytes                            | Format       |
        +--------+----------+----------------------+----------------------------------+--------------+
        |        |          |                      |                                  | sized_string |
        |  0     | --size-- | 24                   | 18                               | uint8        |
        |  1     |          | <insufficient bytes> | 48 65 6c 6c 6f 20 57 6f 72 6c 64 | ascii        |
        +--------+----------+----------------------+----------------------------------+--------------+

        InsufficientMemoryError occurred during unpack operation:

        1 too few bytes to unpack 'ascii' (12 needed, only 11 available)
        """
        ),
    )
