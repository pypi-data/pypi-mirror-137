# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# Copyright 2021 Daniel Mark Gass, see __about__.py for license information.
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
"""Test transform base class."""

# anomaly in pylint: disable=no-member

import pytest
from baseline import Baseline

from plum.conformance import wrap_message
from plum.exceptions import ExcessMemoryError, UnpackError
from plum.littleendian import uint16


class TestExcessBytes:

    """Test unpack dump properly formats larger quantity of extra bytes."""

    def test_unpack_error(self):
        """Exercise formatting all of the excessive bytes."""
        expected_message = Baseline(
            """
            +--------+----------------+-------------------------------------------------+--------+
            | Offset | Value          | Bytes                                           | Format |
            +--------+----------------+-------------------------------------------------+--------+
            |  0     | 39321          | 99 99                                           | uint16 |
            +--------+----------------+-------------------------------------------------+--------+
            |  2     | <excess bytes> | 99 99 99 99 99 99 99 99 99 99 99 99 99 99 99 99 |        |
            | 18     |                | 99 99 99 99                                     |        |
            +--------+----------------+-------------------------------------------------+--------+

            ExcessMemoryError occurred during unpack operation:

            20 unconsumed bytes
            """
        )
        with pytest.raises(UnpackError) as trap:
            uint16.unpack(b"\x99" * 22)

        assert wrap_message(trap.value) == expected_message
        assert isinstance(trap.value.__context__, ExcessMemoryError)
