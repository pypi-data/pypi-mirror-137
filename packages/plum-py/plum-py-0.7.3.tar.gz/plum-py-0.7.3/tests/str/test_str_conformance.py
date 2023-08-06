# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# Copyright 2021 Daniel Mark Gass, see __about__.py for license information.
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
"""Test StrX transform API conformance."""

from baseline import Baseline

from plum.conformance import Case, CaseData
from plum.str import StrX

ascii_sized = StrX("ascii_sized", nbytes=43, encoding="ascii")
ascii_padded = StrX("ascii_padded", nbytes=45, encoding="ascii", pad=b"\x00")
ascii_zero = StrX("ascii_zero", encoding="ascii", zero_termination=True)
ascii_greedy = StrX("ascii_greedy", encoding="ascii")


class TestSized(Case):

    data = CaseData(
        fmt=ascii_sized,
        bindata=b"the quick brown fox jumps over the lazy dog",
        nbytes=43,
        values=("the quick brown fox jumps over the lazy dog",),
        dump=Baseline(
            """
            +--------+---------+--------------------+-------------------------------------------------+-------------+
            | Offset | Access  | Value              | Bytes                                           | Format      |
            +--------+---------+--------------------+-------------------------------------------------+-------------+
            |        |         |                    |                                                 | ascii_sized |
            |  0     | [0:16]  | 'the quick brown ' | 74 68 65 20 71 75 69 63 6b 20 62 72 6f 77 6e 20 |             |
            | 16     | [16:32] | 'fox jumps over t' | 66 6f 78 20 6a 75 6d 70 73 20 6f 76 65 72 20 74 |             |
            | 32     | [32:43] | 'he lazy dog'      | 68 65 20 6c 61 7a 79 20 64 6f 67                |             |
            +--------+---------+--------------------+-------------------------------------------------+-------------+
            """
        ),
        excess=Baseline(
            """
            +--------+---------+--------------------+-------------------------------------------------+-------------+
            | Offset | Access  | Value              | Bytes                                           | Format      |
            +--------+---------+--------------------+-------------------------------------------------+-------------+
            |        |         |                    |                                                 | ascii_sized |
            |  0     | [0:16]  | 'the quick brown ' | 74 68 65 20 71 75 69 63 6b 20 62 72 6f 77 6e 20 |             |
            | 16     | [16:32] | 'fox jumps over t' | 66 6f 78 20 6a 75 6d 70 73 20 6f 76 65 72 20 74 |             |
            | 32     | [32:43] | 'he lazy dog'      | 68 65 20 6c 61 7a 79 20 64 6f 67                |             |
            +--------+---------+--------------------+-------------------------------------------------+-------------+
            | 43     |         | <excess bytes>     | 99                                              |             |
            +--------+---------+--------------------+-------------------------------------------------+-------------+

            ExcessMemoryError occurred during unpack operation:

            1 unconsumed bytes
            """
        ),
        shortage=Baseline(
            """
        +--------+----------------------+-------------------------------------------------+-------------+
        | Offset | Value                | Bytes                                           | Format      |
        +--------+----------------------+-------------------------------------------------+-------------+
        |        | <insufficient bytes> |                                                 | ascii_sized |
        |  0     |                      | 74 68 65 20 71 75 69 63 6b 20 62 72 6f 77 6e 20 |             |
        | 16     |                      | 66 6f 78 20 6a 75 6d 70 73 20 6f 76 65 72 20 74 |             |
        | 32     |                      | 68 65 20 6c 61 7a 79 20 64 6f                   |             |
        +--------+----------------------+-------------------------------------------------+-------------+

        InsufficientMemoryError occurred during unpack operation:

        1 too few bytes to unpack 'ascii_sized' (43 needed, only 42 available)
        """
        ),
    )


class TestPad(Case):
    data = CaseData(
        fmt=ascii_padded,
        bindata=b"the quick brown fox jumps over the lazy dog\x00\x00",
        nbytes=45,
        values=("the quick brown fox jumps over the lazy dog",),
        dump=Baseline(
            """
            +--------+---------+--------------------+-------------------------------------------------+--------------+
            | Offset | Access  | Value              | Bytes                                           | Format       |
            +--------+---------+--------------------+-------------------------------------------------+--------------+
            |        |         |                    |                                                 | ascii_padded |
            |  0     | [0:16]  | 'the quick brown ' | 74 68 65 20 71 75 69 63 6b 20 62 72 6f 77 6e 20 |              |
            | 16     | [16:32] | 'fox jumps over t' | 66 6f 78 20 6a 75 6d 70 73 20 6f 76 65 72 20 74 |              |
            | 32     | [32:43] | 'he lazy dog'      | 68 65 20 6c 61 7a 79 20 64 6f 67                |              |
            | 43     | --pad-- |                    | 00 00                                           |              |
            +--------+---------+--------------------+-------------------------------------------------+--------------+
            """
        ),
        excess=Baseline(
            """
            +--------+---------+--------------------+-------------------------------------------------+--------------+
            | Offset | Access  | Value              | Bytes                                           | Format       |
            +--------+---------+--------------------+-------------------------------------------------+--------------+
            |        |         |                    |                                                 | ascii_padded |
            |  0     | [0:16]  | 'the quick brown ' | 74 68 65 20 71 75 69 63 6b 20 62 72 6f 77 6e 20 |              |
            | 16     | [16:32] | 'fox jumps over t' | 66 6f 78 20 6a 75 6d 70 73 20 6f 76 65 72 20 74 |              |
            | 32     | [32:43] | 'he lazy dog'      | 68 65 20 6c 61 7a 79 20 64 6f 67                |              |
            | 43     | --pad-- |                    | 00 00                                           |              |
            +--------+---------+--------------------+-------------------------------------------------+--------------+
            | 45     |         | <excess bytes>     | 99                                              |              |
            +--------+---------+--------------------+-------------------------------------------------+--------------+

            ExcessMemoryError occurred during unpack operation:

            1 unconsumed bytes
            """
        ),
        shortage=Baseline(
            """
        +--------+----------------------+-------------------------------------------------+--------------+
        | Offset | Value                | Bytes                                           | Format       |
        +--------+----------------------+-------------------------------------------------+--------------+
        |        | <insufficient bytes> |                                                 | ascii_padded |
        |  0     |                      | 74 68 65 20 71 75 69 63 6b 20 62 72 6f 77 6e 20 |              |
        | 16     |                      | 66 6f 78 20 6a 75 6d 70 73 20 6f 76 65 72 20 74 |              |
        | 32     |                      | 68 65 20 6c 61 7a 79 20 64 6f 67 00             |              |
        +--------+----------------------+-------------------------------------------------+--------------+

        InsufficientMemoryError occurred during unpack operation:

        1 too few bytes to unpack 'ascii_padded' (45 needed, only 44
        available)
        """
        ),
    )


class TestZeroTerm(Case):

    data = CaseData(
        fmt=ascii_zero,
        bindata=b"the quick brown fox jumps over the lazy dog\x00",
        nbytes=None,
        values=("the quick brown fox jumps over the lazy dog",),
        dump=Baseline(
            """
            +--------+-----------------+--------------------+-------------------------------------------------+------------+
            | Offset | Access          | Value              | Bytes                                           | Format     |
            +--------+-----------------+--------------------+-------------------------------------------------+------------+
            |        |                 |                    |                                                 | ascii_zero |
            |  0     | [0:16]          | 'the quick brown ' | 74 68 65 20 71 75 69 63 6b 20 62 72 6f 77 6e 20 |            |
            | 16     | [16:32]         | 'fox jumps over t' | 66 6f 78 20 6a 75 6d 70 73 20 6f 76 65 72 20 74 |            |
            | 32     | [32:43]         | 'he lazy dog'      | 68 65 20 6c 61 7a 79 20 64 6f 67                |            |
            | 43     | --termination-- |                    | 00                                              |            |
            +--------+-----------------+--------------------+-------------------------------------------------+------------+
            """
        ),
        excess=Baseline(
            """
            +--------+-----------------+--------------------+-------------------------------------------------+------------+
            | Offset | Access          | Value              | Bytes                                           | Format     |
            +--------+-----------------+--------------------+-------------------------------------------------+------------+
            |        |                 |                    |                                                 | ascii_zero |
            |  0     | [0:16]          | 'the quick brown ' | 74 68 65 20 71 75 69 63 6b 20 62 72 6f 77 6e 20 |            |
            | 16     | [16:32]         | 'fox jumps over t' | 66 6f 78 20 6a 75 6d 70 73 20 6f 76 65 72 20 74 |            |
            | 32     | [32:43]         | 'he lazy dog'      | 68 65 20 6c 61 7a 79 20 64 6f 67                |            |
            | 43     | --termination-- |                    | 00                                              |            |
            +--------+-----------------+--------------------+-------------------------------------------------+------------+
            | 44     |                 | <excess bytes>     | 99                                              |            |
            +--------+-----------------+--------------------+-------------------------------------------------+------------+

            ExcessMemoryError occurred during unpack operation:

            1 unconsumed bytes
            """
        ),
        shortage=Baseline(
            """
        +--------+---------+--------------------+-------------------------------------------------+------------+
        | Offset | Access  | Value              | Bytes                                           | Format     |
        +--------+---------+--------------------+-------------------------------------------------+------------+
        |        |         |                    |                                                 | ascii_zero |
        |  0     | [0:16]  | 'the quick brown ' | 74 68 65 20 71 75 69 63 6b 20 62 72 6f 77 6e 20 |            |
        | 16     | [16:32] | 'fox jumps over t' | 66 6f 78 20 6a 75 6d 70 73 20 6f 76 65 72 20 74 |            |
        | 32     | [32:43] | 'he lazy dog'      | 68 65 20 6c 61 7a 79 20 64 6f 67                |            |
        +--------+---------+--------------------+-------------------------------------------------+------------+

        InsufficientMemoryError occurred during unpack operation:

        no zero termination present
        """
        ),
    )


class TestGreedy(Case):

    data = CaseData(
        fmt=ascii_greedy,
        bindata=b"the quick brown fox jumps over the lazy dog",
        nbytes=None,
        values=("the quick brown fox jumps over the lazy dog",),
        dump=Baseline(
            """
            +--------+---------+--------------------+-------------------------------------------------+--------------+
            | Offset | Access  | Value              | Bytes                                           | Format       |
            +--------+---------+--------------------+-------------------------------------------------+--------------+
            |        |         |                    |                                                 | ascii_greedy |
            |  0     | [0:16]  | 'the quick brown ' | 74 68 65 20 71 75 69 63 6b 20 62 72 6f 77 6e 20 |              |
            | 16     | [16:32] | 'fox jumps over t' | 66 6f 78 20 6a 75 6d 70 73 20 6f 76 65 72 20 74 |              |
            | 32     | [32:43] | 'he lazy dog'      | 68 65 20 6c 61 7a 79 20 64 6f 67                |              |
            +--------+---------+--------------------+-------------------------------------------------+--------------+
            """
        ),
        excess="N/A",
        shortage="N/A",
    )
