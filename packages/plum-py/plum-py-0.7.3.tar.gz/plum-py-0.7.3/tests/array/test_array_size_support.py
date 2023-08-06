# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# Copyright 2021 Daniel Mark Gass, see __about__.py for license information.
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
"""Test array transform support for structure's dimmed_member."""

from plum.array import ArrayX
from plum.bigendian import uint8
from plum.dump import Dump


class TestUnpack:

    """Test unpack method variants."""

    buffer = b"\x00\x01\x02"
    greedy = ArrayX("greedy", fmt=uint8)

    def test_unpack(self):
        array, _offset = self.greedy.__unpack__(self.buffer, 0, dims=(2,))
        assert array == [0, 1]

    def test_unpack_and_dump(self):
        array, _offset = self.greedy.__unpack_and_dump__(
            self.buffer, 0, Dump(), dims=(2,)
        )
        assert array == [0, 1]
