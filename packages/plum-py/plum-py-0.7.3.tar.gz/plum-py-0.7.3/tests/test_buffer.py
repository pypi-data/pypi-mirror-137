# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# Copyright 2021 Daniel Mark Gass, see __about__.py for license information.
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
"""Test Buffer corner cases."""

import pytest
from baseline import Baseline

from plum.conformance import wrap_message
from plum.buffer import Buffer
from plum.exceptions import UnpackError
from plum.littleendian import uint16


class TestUnpackErrors:

    expected_message = Baseline(
        """
        +--------+----------------------+-------+--------+
        | Offset | Value                | Bytes | Format |
        +--------+----------------------+-------+--------+
        | 0      | <insufficient bytes> | 01    | uint16 |
        +--------+----------------------+-------+--------+

        InsufficientMemoryError occurred during unpack operation:

        1 too few bytes to unpack 'uint16' (2 needed, only 1 available)
        """
    )

    def test_unpack(self):

        with pytest.raises(UnpackError) as trap:
            with Buffer(b"\x01") as buffer:
                buffer.unpack(uint16)

        assert wrap_message(trap.value) == self.expected_message

    def test_unpack_and_dump(self):
        with pytest.raises(UnpackError) as trap:
            with Buffer(b"\x01") as buffer:
                buffer.unpack_and_dump(uint16)

        assert wrap_message(trap.value) == self.expected_message
