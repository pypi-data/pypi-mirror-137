# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# Copyright 2021 Daniel Mark Gass, see __about__.py for license information.
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
"""Test int transform API conformance."""

from baseline import Baseline

from plum.bigendian import uint16
from plum.conformance import Case, CaseData
from plum.littleendian import uint8, sint32


class TestU16(Case):

    """Test unsigned 16 bit big endian Int."""

    data = CaseData(
        fmt=uint16,
        bindata=b"\x01\x02",
        nbytes=2,
        values=(0x0102,),
        dump=Baseline(
            """
            +--------+-------+-------+--------+
            | Offset | Value | Bytes | Format |
            +--------+-------+-------+--------+
            | 0      | 258   | 01 02 | uint16 |
            +--------+-------+-------+--------+
            """
        ),
        excess=Baseline(
            """
            +--------+----------------+-------+--------+
            | Offset | Value          | Bytes | Format |
            +--------+----------------+-------+--------+
            | 0      | 258            | 01 02 | uint16 |
            +--------+----------------+-------+--------+
            | 2      | <excess bytes> | 99    |        |
            +--------+----------------+-------+--------+

            ExcessMemoryError occurred during unpack operation:

            1 unconsumed bytes
            """
        ),
        shortage=Baseline(
            """
            +--------+----------------------+-------+--------+
            | Offset | Value                | Bytes | Format |
            +--------+----------------------+-------+--------+
            | 0      | <insufficient bytes> | 01    | uint16 |
            +--------+----------------------+-------+--------+

            InsufficientMemoryError occurred during unpack operation:

            1 too few bytes to unpack 'uint16' (2 needed, only 1 available)
            """
        ),
    )


class TestU8(Case):

    """Test unsigned 8 bit little endiant Int."""

    data = CaseData(
        fmt=uint8,
        bindata=b"\x00",
        nbytes=1,
        values=(0,),
        dump=Baseline(
            """
            +--------+-------+-------+--------+
            | Offset | Value | Bytes | Format |
            +--------+-------+-------+--------+
            | 0      | 0     | 00    | uint8  |
            +--------+-------+-------+--------+
            """
        ),
        excess=Baseline(
            """
            +--------+----------------+-------+--------+
            | Offset | Value          | Bytes | Format |
            +--------+----------------+-------+--------+
            | 0      | 0              | 00    | uint8  |
            +--------+----------------+-------+--------+
            | 1      | <excess bytes> | 99    |        |
            +--------+----------------+-------+--------+

            ExcessMemoryError occurred during unpack operation:

            1 unconsumed bytes
            """
        ),
        shortage=Baseline(
            """
            +--------+----------------------+-------+--------+
            | Offset | Value                | Bytes | Format |
            +--------+----------------------+-------+--------+
            |        | <insufficient bytes> |       | uint8  |
            +--------+----------------------+-------+--------+

            InsufficientMemoryError occurred during unpack operation:

            1 too few bytes to unpack 'uint8' (1 needed, only 0 available)
            """
        ),
    )


class TestS32L(Case):

    """Test signed 32 bit little endian integer."""

    data = CaseData(
        fmt=sint32,
        bindata=b"\x00\xfc\xff\xff",
        nbytes=4,
        values=(-1024,),
        dump=Baseline(
            """
            +--------+-------+-------------+--------+
            | Offset | Value | Bytes       | Format |
            +--------+-------+-------------+--------+
            | 0      | -1024 | 00 fc ff ff | sint32 |
            +--------+-------+-------------+--------+
            """
        ),
        excess=Baseline(
            """
            +--------+----------------+-------------+--------+
            | Offset | Value          | Bytes       | Format |
            +--------+----------------+-------------+--------+
            | 0      | -1024          | 00 fc ff ff | sint32 |
            +--------+----------------+-------------+--------+
            | 4      | <excess bytes> | 99          |        |
            +--------+----------------+-------------+--------+

            ExcessMemoryError occurred during unpack operation:

            1 unconsumed bytes
            """
        ),
        shortage=Baseline(
            """
            +--------+----------------------+----------+--------+
            | Offset | Value                | Bytes    | Format |
            +--------+----------------------+----------+--------+
            | 0      | <insufficient bytes> | 00 fc ff | sint32 |
            +--------+----------------------+----------+--------+

            InsufficientMemoryError occurred during unpack operation:

            1 too few bytes to unpack 'sint32' (4 needed, only 3 available)
            """
        ),
    )
