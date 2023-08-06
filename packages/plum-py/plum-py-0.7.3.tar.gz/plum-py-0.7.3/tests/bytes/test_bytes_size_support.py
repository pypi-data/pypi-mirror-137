# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# Copyright 2021 Daniel Mark Gass, see __about__.py for license information.
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
"""Test bytes transform support for structure's sized_member()."""

from plum.dump import Dump
from plum.bytes import BytesX


greedy_bytes = BytesX("greedy_bytes")


class TestUnpack:

    """Test unpack method variants."""

    buffer = b"\x00\x01\x02"

    def test_unpack(self):
        array, _offset = greedy_bytes.__unpack__(self.buffer, 0, nbytes=2)
        assert array == self.buffer[0:2]

    def test_unpack_and_dump(self):
        array, _offset = greedy_bytes.__unpack_and_dump__(
            self.buffer, 0, Dump(), nbytes=2
        )
        assert array == self.buffer[0:2]
