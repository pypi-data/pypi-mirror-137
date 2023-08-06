# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# Copyright 2021 Daniel Mark Gass, see __about__.py for license information.
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
"""Test SizedX transform API conformance."""

import pytest

from baseline import Baseline

from plum.conformance import Case, CaseData, wrap_message
from plum.exceptions import UnpackError
from plum.littleendian import uint8
from plum.sized import SizedX
from plum.str import StrX


ascii_greedy = StrX("ascii", encoding="ascii")

sized_string = SizedX("sized_string", fmt=ascii_greedy, size_fmt=uint8)


class TestApi(Case):

    data = CaseData(
        fmt=sized_string,
        bindata=b"\x0cHello World!",
        nbytes=None,
        values=["Hello World!"],
        dump=Baseline(
            """
            +--------+----------+----------------+-------------------------------------+--------------+
            | Offset | Access   | Value          | Bytes                               | Format       |
            +--------+----------+----------------+-------------------------------------+--------------+
            |        |          |                |                                     | sized_string |
            |  0     | --size-- | 12             | 0c                                  | uint8        |
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
            |  0     | --size-- | 12             | 0c                                  | uint8        |
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
        |  0     | --size-- | 12                   | 0c                               | uint8        |
        |  1     |          | <insufficient bytes> | 48 65 6c 6c 6f 20 57 6f 72 6c 64 | ascii        |
        +--------+----------+----------------------+----------------------------------+--------------+

        InsufficientMemoryError occurred during unpack operation:

        1 too few bytes to unpack 'ascii' (12 needed, only 11 available)
        """
        ),
    )


class TestExceptions:

    """Test special exception cases."""

    def test_excess_bytes(self):
        """Test outer limit more restrictive than inner limit (string case)."""
        sized_int = SizedX("sized_string", fmt=uint8, size_fmt=uint8)

        with pytest.raises(UnpackError) as trap:
            sized_int.unpack(b"\x20" + bytes(32))

        expected = Baseline(
            """
            +--------+----------+----------------+-------------------------------------------------+--------------+
            | Offset | Access   | Value          | Bytes                                           | Format       |
            +--------+----------+----------------+-------------------------------------------------+--------------+
            |        |          |                |                                                 | sized_string |
            |  0     | --size-- | 32             | 20                                              | uint8        |
            |  1     |          | 0              | 00                                              | uint8        |
            +--------+----------+----------------+-------------------------------------------------+--------------+
            |  2     |          | <excess bytes> | 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 |              |
            | 18     |          |                | 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00    |              |
            +--------+----------+----------------+-------------------------------------------------+--------------+

            ExcessMemoryError occurred during unpack operation:

            31 unconsumed bytes
            """
        )

        assert wrap_message(trap.value) == expected
