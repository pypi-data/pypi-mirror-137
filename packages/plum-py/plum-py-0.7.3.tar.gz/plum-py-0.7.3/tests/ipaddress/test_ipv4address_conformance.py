# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# Copyright 2021 Daniel Mark Gass, see __about__.py for license information.
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
"""Test IPv4AddressX transform API conformance."""

from ipaddress import IPv4Address

from baseline import Baseline

from plum.conformance import Case, CaseData
from plum.ipaddress import IPv4AddressX


class TestBigEndian(Case):

    data = CaseData(
        fmt=IPv4AddressX("ipaddr"),
        bindata=bytes.fromhex("00010203"),
        nbytes=4,
        values=(IPv4Address("0.1.2.3"),),
        dump=Baseline(
            """
            +--------+------------------------+-------------+--------+
            | Offset | Value                  | Bytes       | Format |
            +--------+------------------------+-------------+--------+
            | 0      | IPv4Address('0.1.2.3') | 00 01 02 03 | ipaddr |
            +--------+------------------------+-------------+--------+
            """
        ),
        excess=Baseline(
            """
            +--------+------------------------+-------------+--------+
            | Offset | Value                  | Bytes       | Format |
            +--------+------------------------+-------------+--------+
            | 0      | IPv4Address('0.1.2.3') | 00 01 02 03 | ipaddr |
            +--------+------------------------+-------------+--------+
            | 4      | <excess bytes>         | 99          |        |
            +--------+------------------------+-------------+--------+

            ExcessMemoryError occurred during unpack operation:

            1 unconsumed bytes
            """
        ),
        shortage=Baseline(
            """
        +--------+----------------------+----------+--------+
        | Offset | Value                | Bytes    | Format |
        +--------+----------------------+----------+--------+
        | 0      | <insufficient bytes> | 00 01 02 | ipaddr |
        +--------+----------------------+----------+--------+

        InsufficientMemoryError occurred during unpack operation:

        1 too few bytes to unpack 'ipaddr' (4 needed, only 3 available)
        """
        ),
    )


class TestLittleEndian(Case):

    data = CaseData(
        fmt=IPv4AddressX("ipaddr", byteorder="little"),
        bindata=bytes.fromhex("03020100"),
        nbytes=4,
        values=(IPv4Address("0.1.2.3"),),
        dump=Baseline(
            """
            +--------+------------------------+-------------+--------+
            | Offset | Value                  | Bytes       | Format |
            +--------+------------------------+-------------+--------+
            | 0      | IPv4Address('0.1.2.3') | 03 02 01 00 | ipaddr |
            +--------+------------------------+-------------+--------+
            """
        ),
        excess=Baseline(
            """
            +--------+------------------------+-------------+--------+
            | Offset | Value                  | Bytes       | Format |
            +--------+------------------------+-------------+--------+
            | 0      | IPv4Address('0.1.2.3') | 03 02 01 00 | ipaddr |
            +--------+------------------------+-------------+--------+
            | 4      | <excess bytes>         | 99          |        |
            +--------+------------------------+-------------+--------+

            ExcessMemoryError occurred during unpack operation:

            1 unconsumed bytes
            """
        ),
        shortage=Baseline(
            """
        +--------+----------------------+----------+--------+
        | Offset | Value                | Bytes    | Format |
        +--------+----------------------+----------+--------+
        | 0      | <insufficient bytes> | 03 02 01 | ipaddr |
        +--------+----------------------+----------+--------+

        InsufficientMemoryError occurred during unpack operation:

        1 too few bytes to unpack 'ipaddr' (4 needed, only 3 available)
        """
        ),
    )
