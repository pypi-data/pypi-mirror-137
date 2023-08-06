# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# Copyright 2021 Daniel Mark Gass, see __about__.py for license information.
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
"""Test pack() utility function."""

import pytest
from baseline import Baseline

from plum.conformance import wrap_message
from plum.exceptions import PackError
from plum.littleendian import uint8, uint16
from plum.utilities import pack, pack_and_dump


class TestPackHappyPath:

    """Test normal operations packing multiple items in one call."""

    def test_happy_path_single(self):
        """Test packing with single pos instance args."""
        exp_buffer = b"\x02\x01"
        exp_dump = Baseline(
            """
            +--------+-------+-------+--------+
            | Offset | Value | Bytes | Format |
            +--------+-------+-------+--------+
            | 0      | 258   | 02 01 | uint16 |
            +--------+-------+-------+--------+
            """
        )

        fmt = uint16

        assert pack(0x0102, fmt) == exp_buffer

        buffer, dump = pack_and_dump(0x0102, fmt)
        assert (buffer, str(dump)) == (exp_buffer, exp_dump)

    def test_happy_path_items(self):
        """Test packing with pos instance args."""
        exp_buffer = b"\x03\x02\x01"
        exp_dump = Baseline(
            """
            +--------+--------+-------+-------+--------+
            | Offset | Access | Value | Bytes | Format |
            +--------+--------+-------+-------+--------+
            | 0      | [0]    | 3     | 03    | uint8  |
            | 1      | [1]    | 258   | 02 01 | uint16 |
            +--------+--------+-------+-------+--------+
            """
        )

        fmt = (uint8, uint16)

        assert pack((3, 0x0102), fmt) == exp_buffer

        buffer, dump = pack_and_dump((3, 0x0102), fmt)
        assert (buffer, str(dump)) == (exp_buffer, exp_dump)

    def test_happy_path_kwitems(self):
        """Test packing with kw instance args."""
        exp_buffer = b"\x00\x02\x01"
        exp_dump = Baseline(
            """
            +--------+--------+-------+-------+--------+
            | Offset | Access | Value | Bytes | Format |
            +--------+--------+-------+-------+--------+
            | 0      | ['m1'] | 0     | 00    | uint8  |
            | 1      | ['m2'] | 258   | 02 01 | uint16 |
            +--------+--------+-------+-------+--------+
            """
        )

        fmt = {"m1": uint8, "m2": uint16}

        assert pack(dict(m1=0, m2=0x0102), fmt) == exp_buffer

        buffer, dump = pack_and_dump(dict(m1=0, m2=0x0102), fmt)
        assert (buffer, str(dump)) == (exp_buffer, exp_dump)

    def test_happy_path_nested(self):
        """Test packing with both named and unnamed values (nested)."""
        exp_buffer = b"\x00\x02\x01"
        exp_dump = Baseline(
            """
            +--------+--------+-------+-------+--------+
            | Offset | Access | Value | Bytes | Format |
            +--------+--------+-------+-------+--------+
            |        | ['m1'] |       |       |        |
            | 0      |   [0]  | 0     | 00    | uint8  |
            | 1      |   [1]  | 258   | 02 01 | uint16 |
            +--------+--------+-------+-------+--------+
            """
        )

        fmt = {"m1": (uint8, uint16)}

        assert pack(dict(m1=(0, 0x0102)), fmt) == exp_buffer

        buffer, dump = pack_and_dump(dict(m1=(0, 0x0102)), fmt)
        assert (buffer, str(dump)) == (exp_buffer, exp_dump)

    def test_empty_dict_fmt(self):
        """Test packing with both named and unnamed values (nested)."""
        exp_buffer = b""
        exp_dump = Baseline(
            """
            +--------+-------+-------+--------+
            | Offset | Value | Bytes | Format |
            +--------+-------+-------+--------+
            |        |       |       |        |
            +--------+-------+-------+--------+
            """
        )

        fmt = {}

        assert pack({}, fmt) == exp_buffer

        buffer, dump = pack_and_dump({}, fmt)
        assert (buffer, str(dump)) == (exp_buffer, exp_dump)


class TestPlumView:

    """Test pack() operates with plum view types."""

    def test_view_as_pos_argument(self):
        """Test packing with view as positional argument."""
        exp_buffer = b"\x00\x02\x01"
        exp_dump = Baseline(
            """
            +--------+--------+-------+-------+--------+
            | Offset | Access | Value | Bytes | Format |
            +--------+--------+-------+-------+--------+
            | 0      | [0]    | 0     | 00    | uint8  |
            | 1      | [1]    | 258   | 02 01 | uint16 |
            +--------+--------+-------+-------+--------+
            """
        )

        shared_memory = b"\x02\x01\x00"
        uint16_view = uint16.view(shared_memory, offset=0)
        uint8_view = uint8.view(shared_memory, offset=2)

        fmt = (uint8, uint16)

        assert pack((uint8_view, uint16_view), fmt) == exp_buffer

        buffer, dump = pack_and_dump((uint8_view, uint16_view), fmt)
        assert (buffer, str(dump)) == (exp_buffer, exp_dump)

    def test_view_as_kw_argument(self):
        """Test packing with view as keyword argument."""

        exp_buffer = b"\x00\x02\x01"
        exp_dump = Baseline(
            """
            +--------+--------+-------+-------+--------+
            | Offset | Access | Value | Bytes | Format |
            +--------+--------+-------+-------+--------+
            | 0      | ['m1'] | 0     | 00    | uint8  |
            | 1      | ['m2'] | 258   | 02 01 | uint16 |
            +--------+--------+-------+-------+--------+
            """
        )

        shared_memory = b"\x02\x01\x00"
        uint16_view = uint16.view(shared_memory, offset=0)
        uint8_view = uint8.view(shared_memory, offset=2)

        fmt = {"m1": uint8, "m2": uint16}

        assert pack(dict(m1=uint8_view, m2=uint16_view), fmt) == exp_buffer

        buffer, dump = pack_and_dump(dict(m1=uint8_view, m2=uint16_view), fmt)
        assert (buffer, str(dump)) == (exp_buffer, exp_dump)


class TestExceptions:

    """Test pack exception corner cases."""

    def test_bad_single_type(self):
        """Test packing exception with format not a valid choice."""
        expected = Baseline(
            """
            +--------+-------+-------+---------------+
            | Offset | Value | Bytes | Format        |
            +--------+-------+-------+---------------+
            |        | 0     |       | 258 (invalid) |
            +--------+-------+-------+---------------+

            TypeError occurred during pack operation:

            bad item format, must be a packable data type/transform (or a dict,
            list, or tuple of them)
            """
        )

        with pytest.raises(PackError) as trap:
            pack((0, 0x0102))  # bad fmt
        assert wrap_message(trap.value) == expected
        assert isinstance(trap.value.__context__, TypeError)

        with pytest.raises(PackError) as trap:
            pack_and_dump((0, 0x0102))  # bad fmt
        assert wrap_message(trap.value) == expected
        assert isinstance(trap.value.__context__, TypeError)

    def test_bad_tuple_type(self):
        """Test packing exception with invalid type in format tuple."""
        expected = Baseline(
            """
            +--------+--------+-------+-------+-------------+
            | Offset | Access | Value | Bytes | Format      |
            +--------+--------+-------+-------+-------------+
            | 0      | [0]    | 0     | 00    | uint8       |
            |        | [1]    | 258   |       | 0 (invalid) |
            +--------+--------+-------+-------+-------------+

            TypeError occurred during pack operation:

            bad item format, must be a packable data type/transform (or a dict,
            list, or tuple of them)
            """
        )

        with pytest.raises(PackError) as trap:
            pack((0, 0x0102), (uint8, 0))
        assert wrap_message(trap.value) == expected
        assert isinstance(trap.value.__context__, TypeError)

        with pytest.raises(PackError) as trap:
            pack_and_dump((0, 0x0102), (uint8, 0))
        assert wrap_message(trap.value) == expected
        assert isinstance(trap.value.__context__, TypeError)

    def test_bad_dict_type(self):
        """Test packing exception with invalid type in format tuple."""
        expected = Baseline(
            """
            +--------+--------+-------+-------+-------------+
            | Offset | Access | Value | Bytes | Format      |
            +--------+--------+-------+-------+-------------+
            | 0      | ['m1'] | 0     | 00    | uint8       |
            |        | ['m2'] | 258   |       | 0 (invalid) |
            +--------+--------+-------+-------+-------------+

            TypeError occurred during pack operation:

            bad item format, must be a packable data type/transform (or a dict,
            list, or tuple of them)
            """
        )

        fmt = {"m1": uint8, "m2": 0}

        with pytest.raises(PackError) as trap:
            pack(dict(m1=0, m2=0x0102), fmt)
        assert wrap_message(trap.value) == expected
        assert isinstance(trap.value.__context__, TypeError)

        with pytest.raises(PackError) as trap:
            pack_and_dump(dict(m1=0, m2=0x0102), fmt)
        assert wrap_message(trap.value) == expected
        assert isinstance(trap.value.__context__, TypeError)

    def test_args_shortage(self):
        """Test packing exception with not enough positional args."""
        expected = Baseline(
            """
            +--------+--------+-----------+-------+--------+
            | Offset | Access | Value     | Bytes | Format |
            +--------+--------+-----------+-------+--------+
            | 0      | [0]    | 0         | 00    | uint8  |
            |        | [1]    | (missing) |       | uint16 |
            +--------+--------+-----------+-------+--------+

            TypeError occurred during pack operation:

            1 value given, expected 2
            """
        )

        fmt = (uint8, uint16)

        with pytest.raises(PackError) as trap:
            pack([0], fmt)
        assert wrap_message(trap.value) == expected
        assert isinstance(trap.value.__context__, TypeError)

        with pytest.raises(PackError) as trap:
            pack_and_dump([0], fmt)
        assert wrap_message(trap.value) == expected
        assert isinstance(trap.value.__context__, TypeError)

    def test_args_excess(self):
        """Test packing exception with too many positional args."""
        expected = Baseline(
            """
            +--------+--------+-------+-------+--------------+
            | Offset | Access | Value | Bytes | Format       |
            +--------+--------+-------+-------+--------------+
            | 0      | [0]    | 0     | 00    | uint8        |
            | 1      | [1]    | 1     | 01 00 | uint16       |
            +--------+--------+-------+-------+--------------+
            |        | [2]    | 2     |       | (unexpected) |
            +--------+--------+-------+-------+--------------+

            TypeError occurred during pack operation:

            3 values given, expected 2
            """
        )

        fmt = (uint8, uint16)

        with pytest.raises(PackError) as trap:
            pack((0, 1, 2), fmt)
        assert wrap_message(trap.value) == expected
        assert isinstance(trap.value.__context__, TypeError)

        with pytest.raises(PackError) as trap:
            pack_and_dump((0, 1, 2), fmt)
        assert wrap_message(trap.value) == expected
        assert isinstance(trap.value.__context__, TypeError)

    def test_kwargs_shortage(self):
        """Test packing exception with not enough keyword args."""
        expected = Baseline(
            """
            +--------+--------+-----------+-------+--------+
            | Offset | Access | Value     | Bytes | Format |
            +--------+--------+-----------+-------+--------+
            | 0      | ['m1'] | 0         | 00    | uint8  |
            |        | ['m2'] | (missing) |       | uint16 |
            +--------+--------+-----------+-------+--------+

            TypeError occurred during pack operation:

            missing value: 'm2'
            """
        )

        fmt = {"m1": uint8, "m2": uint16}

        with pytest.raises(PackError) as trap:
            pack(dict(m1=0), fmt)
        assert wrap_message(trap.value) == expected
        assert isinstance(trap.value.__context__, TypeError)

        with pytest.raises(PackError) as trap:
            pack_and_dump(dict(m1=0), fmt)
        assert wrap_message(trap.value) == expected
        assert isinstance(trap.value.__context__, TypeError)

    def test_kwargs_excess(self):
        """Test packing exception with too many keyword args."""
        expected = Baseline(
            """
            +--------+--------+-------+-------+--------------+
            | Offset | Access | Value | Bytes | Format       |
            +--------+--------+-------+-------+--------------+
            | 0      | ['m1'] | 0     | 00    | uint8        |
            | 1      | ['m2'] | 1     | 01 00 | uint16       |
            +--------+--------+-------+-------+--------------+
            |        | ['m3'] | 2     |       | (unexpected) |
            +--------+--------+-------+-------+--------------+

            TypeError occurred during pack operation:

            unexpected value: 'm3'
            """
        )

        fmt = {"m1": uint8, "m2": uint16}

        with pytest.raises(PackError) as trap:
            pack(dict(m1=0, m2=1, m3=2), fmt)
        assert wrap_message(trap.value) == expected
        assert isinstance(trap.value.__context__, TypeError)

        with pytest.raises(PackError) as trap:
            pack_and_dump(dict(m1=0, m2=1, m3=2), fmt)
        assert wrap_message(trap.value) == expected
        assert isinstance(trap.value.__context__, TypeError)
