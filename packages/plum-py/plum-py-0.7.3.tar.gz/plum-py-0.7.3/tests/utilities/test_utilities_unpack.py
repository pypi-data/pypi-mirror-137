# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# Copyright 2021 Daniel Mark Gass, see __about__.py for license information.
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
"""Test unpack() utility function."""

from typing import Optional, Tuple

import pytest
from baseline import Baseline

from plum.conformance import wrap_message
from plum.data import Data, DataMeta
from plum.dump import Record
from plum.exceptions import InsufficientMemoryError, ExcessMemoryError, UnpackError
from plum.littleendian import uint8, uint16
from plum.utilities import getbytes, unpack, unpack_and_dump
from plum.structure import Structure, member


class CustomError(Data, metaclass=DataMeta):  # pylint: disable=abstract-method

    """Always raises ValueError when unpacked."""

    @classmethod
    def __unpack__(
        cls, buffer: bytes, offset: int, dump: Optional[Record] = None
    ) -> Tuple[int, int]:
        if dump is not None:
            dump.value = "<invalid>"
            getbytes(buffer, offset, dump, 1)
        raise ValueError("invalid byte")


class CustomStructure(Structure):

    """Has member that raises ValueError when unpacked."""

    m1 = member(fmt=uint16)
    m2 = member(fmt=CustomError)


class TestFormatVariations:

    """Test format variations."""

    def test_plum_type(self):
        """Test format is a plum type."""
        exp_dump = Baseline(
            """
            +--------+-------+-------+--------+
            | Offset | Value | Bytes | Format |
            +--------+-------+-------+--------+
            | 0      | 258   | 02 01 | uint16 |
            +--------+-------+-------+--------+
            """
        )

        buffer = b"\x02\x01"
        fmt = uint16

        item = unpack(fmt, buffer)
        assert item == 0x0102

        item, dump = unpack_and_dump(fmt, buffer)
        assert item == 0x0102
        assert str(dump) == exp_dump

    def test_tuple(self):
        """Test format is a tuple of plum types."""
        exp_dump = Baseline(
            """
            +--------+--------+-------+-------+--------+
            | Offset | Access | Value | Bytes | Format |
            +--------+--------+-------+-------+--------+
            | 0      | [0]    | 2     | 02    | uint8  |
            | 1      | [1]    | 1     | 01    | uint8  |
            +--------+--------+-------+-------+--------+
            """
        )

        buffer = b"\x02\x01"
        fmt = (uint8, uint8)

        item = unpack(fmt, buffer)
        assert item == (2, 1)

        item, dump = unpack_and_dump(fmt, buffer)
        assert item == (2, 1)
        assert str(dump) == exp_dump

    def test_list(self):
        """Test format is a list of plum types."""
        exp_dump = Baseline(
            """
            +--------+--------+-------+-------+--------+
            | Offset | Access | Value | Bytes | Format |
            +--------+--------+-------+-------+--------+
            | 0      | [0]    | 2     | 02    | uint8  |
            | 1      | [1]    | 1     | 01    | uint8  |
            +--------+--------+-------+-------+--------+
            """
        )

        buffer = b"\x02\x01"
        fmt = [uint8, uint8]

        item = unpack(fmt, buffer)
        assert item == [2, 1]

        item, dump = unpack_and_dump(fmt, buffer)
        assert item == [2, 1]
        assert str(dump) == exp_dump

    def test_dict(self):
        """Test format is a dictionary of plum types."""
        exp_dump = Baseline(
            """
            +--------+--------+-------+-------+--------+
            | Offset | Access | Value | Bytes | Format |
            +--------+--------+-------+-------+--------+
            | 0      | ['a']  | 2     | 02    | uint8  |
            | 1      | ['b']  | 1     | 01    | uint8  |
            +--------+--------+-------+-------+--------+
            """
        )

        buffer = b"\x02\x01"
        fmt = {"a": uint8, "b": uint8}

        item = unpack(fmt, buffer)
        assert item == {"a": 2, "b": 1}

        item, dump = unpack_and_dump(fmt, buffer)
        assert item == {"a": 2, "b": 1}
        assert str(dump) == exp_dump

    def test_nested(self):
        """Test format is a dictionary of plum types."""
        exp_dump = Baseline(
            """
            +--------+----------+-------+-------+--------+
            | Offset | Access   | Value | Bytes | Format |
            +--------+----------+-------+-------+--------+
            |        | ['a']    |       |       |        |
            | 0      |   [0]    | 1     | 01    | uint8  |
            | 1      |   [1]    | 2     | 02    | uint8  |
            |        | ['b']    |       |       |        |
            | 2      |   ['i']  | 3     | 03    | uint8  |
            | 3      |   ['ii'] | 4     | 04    | uint8  |
            | 4      | ['c']    | 5     | 05    | uint8  |
            +--------+----------+-------+-------+--------+
            """
        )

        buffer = b"\x01\x02\x03\x04\x05"
        fmt = {"a": (uint8, uint8), "b": {"i": uint8, "ii": uint8}, "c": uint8}

        item = unpack(fmt, buffer)
        assert item == {"a": (1, 2), "b": {"i": 3, "ii": 4}, "c": 5}

        item, dump = unpack_and_dump(fmt, buffer)
        assert item == {"a": (1, 2), "b": {"i": 3, "ii": 4}, "c": 5}
        assert str(dump) == exp_dump


class TestExceptions:

    """Test various exception paths."""

    def test_value_error(self):
        """Verify UnpackError raised with context of original unpacking exception."""
        exp_message = Baseline(
            """
            +--------+--------+-----------+-------+-----------------+
            | Offset | Access | Value     | Bytes | Format          |
            +--------+--------+-----------+-------+-----------------+
            |        |        |           |       | CustomStructure |
            | 0      | m1     | 258       | 02 01 | uint16          |
            | 2      | m2     | <invalid> | 00    | CustomError     |
            +--------+--------+-----------+-------+-----------------+

            ValueError occurred during unpack operation:

            invalid byte
            """
        )
        fmt = CustomStructure
        buffer = b"\x02\x01\x00"

        with pytest.raises(UnpackError) as trap:
            unpack(fmt, buffer)
        assert wrap_message(trap.value) == exp_message
        assert isinstance(trap.value.__context__, ValueError)

        with pytest.raises(UnpackError) as trap:
            unpack_and_dump(fmt, buffer)
        assert wrap_message(trap.value) == exp_message
        assert isinstance(trap.value.__context__, ValueError)


class TestUnpackBytes:

    """Test buffer argument as "bytes" type."""

    # FUTURE - move this to conformance test

    fmt = uint16
    buffer_type = bytes
    buffer_data = b"\x02\x01"
    offset = 0

    exp_value = 0x0102
    exp_dump = Baseline(
        """
        +--------+-------+-------+--------+
        | Offset | Value | Bytes | Format |
        +--------+-------+-------+--------+
        | 0      | 258   | 02 01 | uint16 |
        +--------+-------+-------+--------+
        """
    )

    def test_sample(self):
        """Verify unpack successful."""

        buffer = self.buffer_type(self.buffer_data)
        assert unpack(self.fmt, buffer) == self.exp_value

        buffer = self.buffer_type(self.buffer_data)
        value, dump = unpack_and_dump(self.fmt, buffer)
        assert (value, str(dump)) == (self.exp_value, self.exp_dump)

    exp_insufficient_message = Baseline(
        """
        +--------+----------------------+-------+--------+
        | Offset | Value                | Bytes | Format |
        +--------+----------------------+-------+--------+
        | 0      | <insufficient bytes> | 02    | uint16 |
        +--------+----------------------+-------+--------+

        InsufficientMemoryError occurred during unpack operation:

        1 too few bytes to unpack 'uint16' (2 needed, only 1 available)
        """
    )

    def test_insufficient(self):
        """Verify UnpackError with InsufficientMemoryError context when too few bytes."""
        buffer = self.buffer_type(self.buffer_data[:-1])
        with pytest.raises(UnpackError) as trap:
            unpack(self.fmt, buffer)
        assert wrap_message(trap.value) == self.exp_insufficient_message
        assert isinstance(trap.value.__context__, InsufficientMemoryError)

        buffer = self.buffer_type(self.buffer_data[:-1])
        with pytest.raises(UnpackError) as trap:
            unpack_and_dump(self.fmt, buffer)
        assert wrap_message(trap.value) == self.exp_insufficient_message
        assert isinstance(trap.value.__context__, InsufficientMemoryError)

    exp_excess_message = Baseline(
        """
            +--------+----------------+-------------------------------------------------+--------+
            | Offset | Value          | Bytes                                           | Format |
            +--------+----------------+-------------------------------------------------+--------+
            |  0     | 258            | 02 01                                           | uint16 |
            +--------+----------------+-------------------------------------------------+--------+
            |  2     | <excess bytes> | 99 9a 9b 9c 9d 9e 9f a0 a1 a2 a3 a4 a5 a6 a7 a8 |        |
            | 18     |                | a9 aa ab ac ad ae af b0 b1 b2 b3 b4             |        |
            +--------+----------------+-------------------------------------------------+--------+

            ExcessMemoryError occurred during unpack operation:

            28 unconsumed bytes
            """
    )

    def test_excess(self):
        """Verify UnpackError with ExcessMemoryError context when too many bytes."""
        excess = bytes(range(0x99, 0xB5))
        buffer = self.buffer_type(self.buffer_data + excess)
        with pytest.raises(UnpackError) as trap:
            unpack(self.fmt, buffer)
        assert wrap_message(trap.value) == self.exp_excess_message
        assert isinstance(trap.value.__context__, ExcessMemoryError)

        buffer = self.buffer_type(self.buffer_data + excess)
        with pytest.raises(UnpackError) as trap:
            unpack_and_dump(self.fmt, buffer)
        assert wrap_message(trap.value) == self.exp_excess_message
        assert isinstance(trap.value.__context__, ExcessMemoryError)


class TestUnpackByteArray(TestUnpackBytes):

    """Test buffer argument as "bytearray" type."""

    buffer_type = bytearray
