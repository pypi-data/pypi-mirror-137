# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# Copyright 2021 Daniel Mark Gass, see __about__.py for license information.
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
"""Test Data store base class."""

# anomaly in pylint: disable=no-member

import pytest
from baseline import Baseline

from plum.conformance import wrap_message
from plum.data import Data
from plum.exceptions import ExcessMemoryError, PackError, UnpackError
from plum.littleendian import uint16


class TestRetries:

    """Test pack and unpack error retry and reporting mechanisms."""

    class Custom(Data):
        __nbytes__ = 2

        def __init__(self, value=0):
            self.value = value

        def __int__(self):
            return int(self.value)

        @classmethod
        def __pack__(cls, value, pieces, dump=None):
            if dump is not None:
                dump.value = value
            uint16.__pack__(int(value), pieces, dump)

        @classmethod
        def __unpack__(cls, buffer, offset, dump=None):
            value, offset = uint16.__unpack__(buffer, offset, dump)
            return cls(value), offset

        def __eq__(self, other):
            return int(self) == int(other)

        def __repr__(self):
            return f"{self.value}"

    def test_unpack_error(self):
        """Exercise formatting all of the excessive bytes."""
        expected_message = Baseline(
            """
            +--------+----------------+-------------------------------------------------+--------+
            | Offset | Value          | Bytes                                           | Format |
            +--------+----------------+-------------------------------------------------+--------+
            |  0     | 39321          | 99 99                                           | Custom |
            +--------+----------------+-------------------------------------------------+--------+
            |  2     | <excess bytes> | 99 99 99 99 99 99 99 99 99 99 99 99 99 99 99 99 |        |
            | 18     |                | 99 99 99 99                                     |        |
            +--------+----------------+-------------------------------------------------+--------+

            ExcessMemoryError occurred during unpack operation:

            20 unconsumed bytes
            """
        )
        with pytest.raises(UnpackError) as trap:
            self.Custom.unpack(b"\x99" * 22)

        assert wrap_message(trap.value) == expected_message
        assert isinstance(trap.value.__context__, ExcessMemoryError)

    expected_pack_error = Baseline(
        """
        +--------+-------+-------+--------+
        | Offset | Value | Bytes | Format |
        +--------+-------+-------+--------+
        |        | hello |       | Custom |
        +--------+-------+-------+--------+

        ValueError occurred during pack operation:

        invalid literal for int() with base 10: 'hello'
        """
    )

    def test_pack_error(self):
        with pytest.raises(PackError) as trap:
            self.Custom.pack("hello")

        assert wrap_message(trap.value) == self.expected_pack_error

    def test_ipack_error(self):
        with pytest.raises(PackError) as trap:
            self.Custom("hello").ipack()

        assert wrap_message(trap.value) == self.expected_pack_error

    def test_view(self):
        expected_message = Baseline(
            """
            'Custom' does not support view()
            """
        )
        with pytest.raises(TypeError) as trap:
            self.Custom.view(bytes(2))

        assert wrap_message(trap.value) == expected_message
