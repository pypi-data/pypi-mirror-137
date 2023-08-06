# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# Copyright 2021 Daniel Mark Gass, see __about__.py for license information.
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
"""Test special bytes behaviors of "None" format."""

from baseline import Baseline

from plum.items import ItemsX
from plum.littleendian import uint8
from plum.utilities import pack, pack_and_dump, unpack, unpack_and_dump


class TestSimpleItemMethods:

    """Test pack() and unpack() methods of items transform."""

    items_x = ItemsX("items_x", fmt=None)

    value = bytes(range(20))

    expected_dump = Baseline(
        r"""
        +--------+-----------+---------------------------------------------------------------+-------------------------------------------------+---------+
        | Offset | Access    | Value                                                         | Bytes                                           | Format  |
        +--------+-----------+---------------------------------------------------------------+-------------------------------------------------+---------+
        |        |           |                                                               |                                                 | items_x |
        |        |           |                                                               |                                                 | bytes   |
        |  0     |   [0:16]  | b'\x00\x01\x02\x03\x04\x05\x06\x07\x08\t\n\x0b\x0c\r\x0e\x0f' | 00 01 02 03 04 05 06 07 08 09 0a 0b 0c 0d 0e 0f |         |
        | 16     |   [16:20] | b'\x10\x11\x12\x13'                                           | 10 11 12 13                                     |         |
        +--------+-----------+---------------------------------------------------------------+-------------------------------------------------+---------+
        """
    )

    def test_pack(self):
        buffer = self.items_x.pack(self.value)
        assert buffer == self.value

    def test_pack_and_dump(self):
        buffer, dump = self.items_x.pack_and_dump(self.value)
        assert buffer == self.value
        assert str(dump) == self.expected_dump

    def test_unpack(self):
        item = self.items_x.unpack(self.value)
        assert item == self.value

    def test_unpack_and_dump(self):
        item, dump = self.items_x.unpack_and_dump(self.value)
        assert item == self.value
        assert str(dump) == self.expected_dump


class TestSimpleUtilityFunctions:
    """Test pack() and unpack() utility methods that use items transform."""

    value = bytes(range(20))

    expected_dump = Baseline(
        r"""
        +--------+---------+---------------------------------------------------------------+-------------------------------------------------+--------+
        | Offset | Access  | Value                                                         | Bytes                                           | Format |
        +--------+---------+---------------------------------------------------------------+-------------------------------------------------+--------+
        |        |         |                                                               |                                                 | bytes  |
        |  0     | [0:16]  | b'\x00\x01\x02\x03\x04\x05\x06\x07\x08\t\n\x0b\x0c\r\x0e\x0f' | 00 01 02 03 04 05 06 07 08 09 0a 0b 0c 0d 0e 0f |        |
        | 16     | [16:20] | b'\x10\x11\x12\x13'                                           | 10 11 12 13                                     |        |
        +--------+---------+---------------------------------------------------------------+-------------------------------------------------+--------+
        """
    )

    def test_pack(self):
        buffer = pack(self.value)
        assert buffer == self.value

    def test_pack_and_dump(self):
        buffer, dump = pack_and_dump(self.value)
        assert buffer == self.value
        assert str(dump) == self.expected_dump

    def test_unpack(self):
        fmt = None
        item = unpack(fmt, self.value)
        assert item == self.value

    def test_unpack_and_dump(self):
        fmt = None
        item, dump = unpack_and_dump(fmt, self.value)
        assert item == self.value
        assert str(dump) == self.expected_dump


class TestComplex:

    items_x = ItemsX("items_x", fmt=(uint8, None))

    bindata = bytes(range(20))
    value = 0, bindata[1:]

    expected_dump = Baseline(
        r"""
        +--------+-----------+---------------------------------------------------------------+-------------------------------------------------+---------+
        | Offset | Access    | Value                                                         | Bytes                                           | Format  |
        +--------+-----------+---------------------------------------------------------------+-------------------------------------------------+---------+
        |        |           |                                                               |                                                 | items_x |
        |  0     | [0]       | 0                                                             | 00                                              | uint8   |
        |        | [1]       |                                                               |                                                 | bytes   |
        |  1     |   [0:16]  | b'\x01\x02\x03\x04\x05\x06\x07\x08\t\n\x0b\x0c\r\x0e\x0f\x10' | 01 02 03 04 05 06 07 08 09 0a 0b 0c 0d 0e 0f 10 |         |
        | 17     |   [16:19] | b'\x11\x12\x13'                                               | 11 12 13                                        |         |
        +--------+-----------+---------------------------------------------------------------+-------------------------------------------------+---------+
        """
    )

    def test_pack(self):
        buffer = self.items_x.pack(self.value)
        assert buffer == self.bindata

    def test_pack_and_dump(self):
        buffer, dump = self.items_x.pack_and_dump(self.value)
        assert buffer == self.bindata
        assert str(dump) == self.expected_dump

    def test_unpack(self):
        item = self.items_x.unpack(self.bindata)
        assert item == self.value

    def test_unpack_and_dump(self):
        item, dump = self.items_x.unpack_and_dump(self.bindata)
        assert item == self.value
        assert str(dump) == self.expected_dump
