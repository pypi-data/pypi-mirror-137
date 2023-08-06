# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# Copyright 2021 Daniel Mark Gass, see __about__.py for license information.
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
"""Test base view pack methods."""

from baseline import Baseline

from plum.littleendian import uint16


class TestPack:

    """Test base view pack methods."""

    EXPECT_DUMP = Baseline(
        """
        +--------+-------+-------+--------+
        | Offset | Value | Bytes | Format |
        +--------+-------+-------+--------+
        | 1      | 513   | 01 02 | uint16 |
        +--------+-------+-------+--------+
        """
    )

    def test_pack(self):
        """Test base view pack() method."""
        buffer = bytearray([0, 1, 2, 3])
        view_16 = uint16.view(buffer, offset=1)
        assert view_16.ipack() == b"\x01\x02"

    def test_pack_and_dump(self):
        """Test base view pack_and_dump() method."""
        buffer = bytearray([0, 1, 2, 3])
        view_16 = uint16.view(buffer, offset=1)
        membytes, dump = view_16.ipack_and_dump()
        assert membytes == b"\x01\x02"
        assert str(dump) == self.EXPECT_DUMP
