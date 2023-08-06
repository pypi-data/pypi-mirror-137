# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# Copyright 2021 Daniel Mark Gass, see __about__.py for license information.
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
"""Test bytes transform support for structure's sized_member()."""

import pytest
from baseline import Baseline
from plum.bytes import BytesX
from plum.conformance import wrap_message
from plum.exceptions import PackError

bytes4 = BytesX("bytes4", nbytes=4)


class Test:
    def test_pack(self):
        expected_message = Baseline(
            """
            +--------+--------+----------+----------------+--------+
            | Offset | Access | Value    | Bytes          | Format |
            +--------+--------+----------+----------------+--------+
            |        |        |          |                | bytes4 |
            | 0      | [0:5]  | b'12345' | 31 32 33 34 35 |        |
            +--------+--------+----------+----------------+--------+

            ValueError occurred during pack operation:

            expected length to be 4 but instead found 5
            """
        )

        with pytest.raises(PackError) as trap:
            bytes4.pack(b"12345")

        assert wrap_message(trap.value) == expected_message
