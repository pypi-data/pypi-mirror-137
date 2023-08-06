# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# Copyright 2021 Daniel Mark Gass, see __about__.py for license information.
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
"""Test array transform API conformance."""

from baseline import Baseline

from plum.array import ArrayX
from plum.conformance import Case, CaseData
from plum.littleendian import uint8
from plum.str import StrX

ascii_zero = StrX("ascii_zero", encoding="ascii", zero_termination=True)


class TestFixedGreedy(Case):

    """Test greedy with fixed size members."""

    data = CaseData(
        fmt=ArrayX("greedy", fmt=uint8),
        bindata=bytes(range(4)),
        nbytes=None,
        values=(list(range(4)), tuple(range(4))),
        dump=Baseline(
            """
            +--------+--------+-------+-------+--------+
            | Offset | Access | Value | Bytes | Format |
            +--------+--------+-------+-------+--------+
            |        |        |       |       | greedy |
            | 0      | [0]    | 0     | 00    | uint8  |
            | 1      | [1]    | 1     | 01    | uint8  |
            | 2      | [2]    | 2     | 02    | uint8  |
            | 3      | [3]    | 3     | 03    | uint8  |
            +--------+--------+-------+-------+--------+
            """
        ),
        excess="N/A",
        shortage="N/A",
    )


class TestVariableGreedy(Case):

    """Test greedy with variable sized members."""

    data = CaseData(
        fmt=ArrayX("strarray", fmt=ascii_zero),
        bindata=b"Hello\x00World!\x00",
        nbytes=None,
        values=(
            ["Hello", "World!"],  # list
            ("Hello", "World!"),  # tuple
        ),
        dump=Baseline(
            """
            +--------+-------------------+----------+-------------------+------------+
            | Offset | Access            | Value    | Bytes             | Format     |
            +--------+-------------------+----------+-------------------+------------+
            |        |                   |          |                   | strarray   |
            |        | [0]               |          |                   | ascii_zero |
            |  0     |   [0:5]           | 'Hello'  | 48 65 6c 6c 6f    |            |
            |  5     |   --termination-- |          | 00                |            |
            |        | [1]               |          |                   | ascii_zero |
            |  6     |   [0:6]           | 'World!' | 57 6f 72 6c 64 21 |            |
            | 12     |   --termination-- |          | 00                |            |
            +--------+-------------------+----------+-------------------+------------+
            """
        ),
        excess="N/A",
        shortage=Baseline(
            """
            +--------+-------------------+----------+-------------------+------------+
            | Offset | Access            | Value    | Bytes             | Format     |
            +--------+-------------------+----------+-------------------+------------+
            |        |                   |          |                   | strarray   |
            |        | [0]               |          |                   | ascii_zero |
            |  0     |   [0:5]           | 'Hello'  | 48 65 6c 6c 6f    |            |
            |  5     |   --termination-- |          | 00                |            |
            |        | [1]               |          |                   | ascii_zero |
            |  6     |   [0:6]           | 'World!' | 57 6f 72 6c 64 21 |            |
            +--------+-------------------+----------+-------------------+------------+

            InsufficientMemoryError occurred during unpack operation:

            no zero termination present
            """
        ),
    )


class TestFixedDimmed(Case):

    """Test dimmed array with fixed size members."""

    data = CaseData(
        fmt=ArrayX("array2x2", fmt=uint8, dims=(2, 2)),
        bindata=bytes(range(4)),
        nbytes=4,
        values=(
            [[0, 1], [2, 3]],  # lists
            ((0, 1), (2, 3)),  # tuples
        ),
        dump=Baseline(
            """
            +--------+--------+-------+-------+----------+
            | Offset | Access | Value | Bytes | Format   |
            +--------+--------+-------+-------+----------+
            |        |        |       |       | array2x2 |
            |        | [0]    |       |       |          |
            | 0      |   [0]  | 0     | 00    | uint8    |
            | 1      |   [1]  | 1     | 01    | uint8    |
            |        | [1]    |       |       |          |
            | 2      |   [0]  | 2     | 02    | uint8    |
            | 3      |   [1]  | 3     | 03    | uint8    |
            +--------+--------+-------+-------+----------+
            """
        ),
        excess=Baseline(
            """
            +--------+--------+----------------+-------+----------+
            | Offset | Access | Value          | Bytes | Format   |
            +--------+--------+----------------+-------+----------+
            |        |        |                |       | array2x2 |
            |        | [0]    |                |       |          |
            | 0      |   [0]  | 0              | 00    | uint8    |
            | 1      |   [1]  | 1              | 01    | uint8    |
            |        | [1]    |                |       |          |
            | 2      |   [0]  | 2              | 02    | uint8    |
            | 3      |   [1]  | 3              | 03    | uint8    |
            +--------+--------+----------------+-------+----------+
            | 4      |        | <excess bytes> | 99    |          |
            +--------+--------+----------------+-------+----------+

            ExcessMemoryError occurred during unpack operation:

            1 unconsumed bytes
            """
        ),
        shortage=Baseline(
            """
        +--------+--------+----------------------+-------+----------+
        | Offset | Access | Value                | Bytes | Format   |
        +--------+--------+----------------------+-------+----------+
        |        |        |                      |       | array2x2 |
        |        | [0]    |                      |       |          |
        | 0      |   [0]  | 0                    | 00    | uint8    |
        | 1      |   [1]  | 1                    | 01    | uint8    |
        |        | [1]    |                      |       |          |
        | 2      |   [0]  | 2                    | 02    | uint8    |
        |        |   [1]  | <insufficient bytes> |       | uint8    |
        +--------+--------+----------------------+-------+----------+

        InsufficientMemoryError occurred during unpack operation:

        1 too few bytes to unpack 'uint8' (1 needed, only 0 available)
        """
        ),
    )


class TestVariableDimmed(Case):

    """Test dimmed array with variable size members."""

    data = CaseData(
        fmt=ArrayX("strarray", fmt=ascii_zero, dims=(2,)),
        bindata=b"Hello\x00World!\x00",
        nbytes=None,
        values=(
            ["Hello", "World!"],  # list
            ("Hello", "World!"),  # tuple
        ),
        dump=Baseline(
            """
            +--------+-------------------+----------+-------------------+------------+
            | Offset | Access            | Value    | Bytes             | Format     |
            +--------+-------------------+----------+-------------------+------------+
            |        |                   |          |                   | strarray   |
            |        | [0]               |          |                   | ascii_zero |
            |  0     |   [0:5]           | 'Hello'  | 48 65 6c 6c 6f    |            |
            |  5     |   --termination-- |          | 00                |            |
            |        | [1]               |          |                   | ascii_zero |
            |  6     |   [0:6]           | 'World!' | 57 6f 72 6c 64 21 |            |
            | 12     |   --termination-- |          | 00                |            |
            +--------+-------------------+----------+-------------------+------------+
            """
        ),
        excess=Baseline(
            """
            +--------+-------------------+----------------+-------------------+------------+
            | Offset | Access            | Value          | Bytes             | Format     |
            +--------+-------------------+----------------+-------------------+------------+
            |        |                   |                |                   | strarray   |
            |        | [0]               |                |                   | ascii_zero |
            |  0     |   [0:5]           | 'Hello'        | 48 65 6c 6c 6f    |            |
            |  5     |   --termination-- |                | 00                |            |
            |        | [1]               |                |                   | ascii_zero |
            |  6     |   [0:6]           | 'World!'       | 57 6f 72 6c 64 21 |            |
            | 12     |   --termination-- |                | 00                |            |
            +--------+-------------------+----------------+-------------------+------------+
            | 13     |                   | <excess bytes> | 99                |            |
            +--------+-------------------+----------------+-------------------+------------+

            ExcessMemoryError occurred during unpack operation:

            1 unconsumed bytes
            """
        ),
        shortage=Baseline(
            """
            +--------+-------------------+----------+-------------------+------------+
            | Offset | Access            | Value    | Bytes             | Format     |
            +--------+-------------------+----------+-------------------+------------+
            |        |                   |          |                   | strarray   |
            |        | [0]               |          |                   | ascii_zero |
            |  0     |   [0:5]           | 'Hello'  | 48 65 6c 6c 6f    |            |
            |  5     |   --termination-- |          | 00                |            |
            |        | [1]               |          |                   | ascii_zero |
            |  6     |   [0:6]           | 'World!' | 57 6f 72 6c 64 21 |            |
            +--------+-------------------+----------+-------------------+------------+

            InsufficientMemoryError occurred during unpack operation:

            no zero termination present
            """
        ),
    )
