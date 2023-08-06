# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# Copyright 2021 Daniel Mark Gass, see __about__.py for license information.
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
"""Test AttrDictX transform API conformance."""

from baseline import Baseline

from plum.conformance import Case, CaseData
from plum.attrdict import AttrDict, AttrDictX
from plum.littleendian import uint8, uint16


class Test(Case):

    data = CaseData(
        fmt=AttrDictX({"k1": uint8, "k2": uint16}),
        bindata=bytes.fromhex("000102"),
        nbytes=3,
        values=(AttrDict(k1=0, k2=0x201), dict(k1=0, k2=0x201)),
        dump=Baseline(
            """
            +--------+--------+-------+-------+----------+
            | Offset | Access | Value | Bytes | Format   |
            +--------+--------+-------+-------+----------+
            |        |        |       |       | AttrDict |
            | 0      | k1     | 0     | 00    | uint8    |
            | 1      | k2     | 513   | 01 02 | uint16   |
            +--------+--------+-------+-------+----------+
            """
        ),
        excess=Baseline(
            """
            +--------+--------+----------------+-------+----------+
            | Offset | Access | Value          | Bytes | Format   |
            +--------+--------+----------------+-------+----------+
            |        |        |                |       | AttrDict |
            | 0      | k1     | 0              | 00    | uint8    |
            | 1      | k2     | 513            | 01 02 | uint16   |
            +--------+--------+----------------+-------+----------+
            | 3      |        | <excess bytes> | 99    |          |
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
        |        |        |                      |       | AttrDict |
        | 0      | k1     | 0                    | 00    | uint8    |
        | 1      | k2     | <insufficient bytes> | 01    | uint16   |
        +--------+--------+----------------------+-------+----------+

        InsufficientMemoryError occurred during unpack operation:

        1 too few bytes to unpack 'uint16' (2 needed, only 1 available)
        """
        ),
    )
