# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# Copyright 2021 Daniel Mark Gass, see __about__.py for license information.
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
"""Test NoneX transform API conformance."""

from baseline import Baseline

from plum.conformance import Case, CaseData
from plum.none import NoneX


class Test(Case):

    data = CaseData(
        fmt=NoneX("none"),
        bindata=b"",
        nbytes=0,
        values=(None,),
        dump=Baseline(
            """
            +--------+-------+-------+--------+
            | Offset | Value | Bytes | Format |
            +--------+-------+-------+--------+
            |        | None  |       | none   |
            +--------+-------+-------+--------+
            """
        ),
        excess=Baseline(
            """
            +--------+----------------+-------+--------+
            | Offset | Value          | Bytes | Format |
            +--------+----------------+-------+--------+
            |        | None           |       | none   |
            +--------+----------------+-------+--------+
            | 0      | <excess bytes> | 99    |        |
            +--------+----------------+-------+--------+

            ExcessMemoryError occurred during unpack operation:

            1 unconsumed bytes
            """
        ),
        shortage="N/A",
    )
