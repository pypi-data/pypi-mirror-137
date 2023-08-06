# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# Copyright 2021 Daniel Mark Gass, see __about__.py for license information.
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
"""Test items transform with fmt=None and with tuple pairing."""

import pytest
from baseline import Baseline

from plum.conformance import wrap_message
from plum.exceptions import PackError
from plum.items import items
from plum.littleendian import uint8
from plum.utilities import pack_and_dump


class Test:

    sample_pair = (1, uint8)

    def test_pack(self):
        assert items.pack(self.sample_pair) == bytes.fromhex("01")

    def test_pack_and_dump_method(self):
        expected_dump = Baseline(
            """
            +--------+-------+-------+--------+
            | Offset | Value | Bytes | Format |
            +--------+-------+-------+--------+
            | 0      | 1     | 01    | uint8  |
            +--------+-------+-------+--------+
            """
        )

        memory, dump = items.pack_and_dump(self.sample_pair)

        assert memory == bytes.fromhex("01")
        assert str(dump) == expected_dump

    def test_pack_and_dump_utility(self):
        expected_dump = Baseline(
            """
            +--------+-------+-------+--------+
            | Offset | Value | Bytes | Format |
            +--------+-------+-------+--------+
            | 0      | 1     | 01    | uint8  |
            +--------+-------+-------+--------+
            """
        )

        memory, dump = pack_and_dump(self.sample_pair)

        assert memory == bytes.fromhex("01")
        assert str(dump) == expected_dump

    def test_bad_item_in_method(self):
        expected = Baseline(
            """
            +--------+-------+-------+--------+
            | Offset | Value | Bytes | Format |
            +--------+-------+-------+--------+
            |        | (0,)  |       | tuple  |
            +--------+-------+-------+--------+

            ValueError occurred during pack operation:

            expected (value, fmt) pair, but got tuple of length 1
            """
        )

        with pytest.raises(PackError) as trap:
            items.pack((0,))

        assert wrap_message(trap.value) == expected
        assert isinstance(trap.value.__context__, ValueError)

    def test_bad_item_in_utility(self):
        expected = Baseline(
            """
            +--------+-------+-------+--------+
            | Offset | Value | Bytes | Format |
            +--------+-------+-------+--------+
            |        | (0,)  |       | tuple  |
            +--------+-------+-------+--------+

            ValueError occurred during pack operation:

            expected (value, fmt) pair, but got tuple of length 1
            """
        )

        with pytest.raises(PackError) as trap:
            pack_and_dump((0,))

        assert wrap_message(trap.value) == expected
        assert isinstance(trap.value.__context__, ValueError)
