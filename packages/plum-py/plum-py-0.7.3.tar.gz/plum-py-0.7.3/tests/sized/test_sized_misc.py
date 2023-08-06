# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# Copyright 2021 Daniel Mark Gass, see __about__.py for license information.
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
"""Test SizedX transform API conformance."""

import pytest

from baseline import Baseline

from plum.conformance import wrap_message
from plum.exceptions import UnpackError
from plum.littleendian import uint8
from plum.sized import SizedX
from plum.str import StrX


ascii_greedy = StrX("ascii", encoding="ascii")

sized_string = SizedX(
    "sized_string", fmt=ascii_greedy, size_fmt=uint8, size_access="--nbytes--"
)


class TestSizeAccess:

    """Test customization of size access description."""

    expected_dump = Baseline(
        """
        +--------+------------+----------------+-------------------------------------+--------------+
        | Offset | Access     | Value          | Bytes                               | Format       |
        +--------+------------+----------------+-------------------------------------+--------------+
        |        |            |                |                                     | sized_string |
        |  0     | --nbytes-- | 12             | 0c                                  | uint8        |
        |        |            |                |                                     | ascii        |
        |  1     | [0:12]     | 'Hello World!' | 48 65 6c 6c 6f 20 57 6f 72 6c 64 21 |              |
        +--------+------------+----------------+-------------------------------------+--------------+
        """
    )

    bindata = b"\x0cHello World!"

    def test_pack_dump(self):
        _bindata, dump = sized_string.pack_and_dump("Hello World!")
        assert str(dump) == self.expected_dump

    def test_unpack_dump(self):
        _value, dump = sized_string.unpack_and_dump(self.bindata)
        assert str(dump) == self.expected_dump


class TestExceptions:

    """Test special exception cases."""

    def test_excess_bytes(self):
        """Test outer limit more restrictive than inner limit (string case)."""
        sized_int = SizedX("sized_string", fmt=uint8, size_fmt=uint8)

        with pytest.raises(UnpackError) as trap:
            sized_int.unpack(b"\x20" + bytes(32))

        expected = Baseline(
            """
            +--------+----------+----------------+-------------------------------------------------+--------------+
            | Offset | Access   | Value          | Bytes                                           | Format       |
            +--------+----------+----------------+-------------------------------------------------+--------------+
            |        |          |                |                                                 | sized_string |
            |  0     | --size-- | 32             | 20                                              | uint8        |
            |  1     |          | 0              | 00                                              | uint8        |
            +--------+----------+----------------+-------------------------------------------------+--------------+
            |  2     |          | <excess bytes> | 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 |              |
            | 18     |          |                | 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00    |              |
            +--------+----------+----------------+-------------------------------------------------+--------------+

            ExcessMemoryError occurred during unpack operation:

            31 unconsumed bytes
            """
        )

        assert wrap_message(trap.value) == expected


class TestSizedProperties:

    """Test SizedX properties."""

    def test_fmt(self):
        assert sized_string.fmt is ascii_greedy

    def test_offset(self):
        assert sized_string.offset == 0

    def test_ratio(self):
        assert sized_string.ratio == 1

    def test_size_access(self):
        assert sized_string.size_access == "--nbytes--"

    def test_size_fmt(self):
        assert sized_string.size_fmt is uint8
