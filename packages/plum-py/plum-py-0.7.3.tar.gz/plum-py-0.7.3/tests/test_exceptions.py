# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# Copyright 2021 Daniel Mark Gass, see __about__.py for license information.
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
"""Test special functionality of plum exception types."""

import pytest
from baseline import Baseline

from plum.conformance import wrap_message
from plum.exceptions import ImplementationError, PackError, UnpackError
from plum.littleendian import uint8
from plum.structure import Structure
from plum.utilities import pack, unpack


class TestImplementationError:

    """Test ImplementationError() exception type."""

    def test_custom_message(self):
        """Test uses message specified."""
        exc = ImplementationError("Hello World!")
        assert str(exc) == "Hello World!"

    def test_default_message(self):
        """Test uses a pre-canned message if no message specified."""
        exc = ImplementationError()

        expected = Baseline(
            """
        One of the plum types used in the pack/unpack operation contains an
        implementation error. The operation generated an exception when first
        performed without a dump (for efficiency). But when the operation was
        repeated with a dump (for a better exception message) the exception
        did not re-occur. Please report the inconsistent behavior to the type
        developer.
        """
        )

        assert wrap_message(str(exc)) == expected


class TestPackExceptions:

    """Test invalid format and value combinations when packing."""

    def test_value_not_dict(self):
        """Test value is not a dictionary when format was dict."""
        expected_message = Baseline(
            """


            +--------+-----------+-------+-------+--------+
            | Offset | Access    | Value | Bytes | Format |
            +--------+-----------+-------+-------+--------+
            |        | ['outer'] | 0     |       | dict   |
            +--------+-----------+-------+-------+--------+

            TypeError occurred during pack operation:

            invalid value, expected dict, got 0
            """
        )

        with pytest.raises(PackError) as trap:
            pack(dict(outer=0), {"outer": {"inner": uint8}})

        assert str(trap.value) == expected_message

    def test_value_not_list_like(self):
        """Test value is not a list or tuple when format called for it."""
        expected_message = Baseline(
            """


            +--------+-------+-------+---------------+
            | Offset | Value | Bytes | Format        |
            +--------+-------+-------+---------------+
            |        | 0     |       | tuple or list |
            +--------+-------+-------+---------------+

            TypeError occurred during pack operation:

            invalid value, expected list or tuple, got 0
            """
        )

        with pytest.raises(PackError) as trap:
            pack(0, [[uint8]])

        assert str(trap.value) == expected_message

    def test_fmt_not_valid_value_missing(self):
        """Test format is not a DataMeta when value reported missing."""
        with pytest.raises(PackError) as trap:
            pack({"m1": 0}, {"m1": uint8, "m2": "junk"})

        expected_message = Baseline(
            """


            +--------+--------+-----------+-------+--------+
            | Offset | Access | Value     | Bytes | Format |
            +--------+--------+-----------+-------+--------+
            | 0      | ['m1'] | 0         | 00    | uint8  |
            |        | ['m2'] | (missing) |       |        |
            +--------+--------+-----------+-------+--------+

            TypeError occurred during pack operation:

            missing value: 'm2'
            """
        )

        assert str(trap.value) == expected_message

    def test_multiple_values_missing(self):
        """Test when value has multiple missing members."""
        with pytest.raises(PackError) as trap:
            pack({"m1": 0}, {"m1": uint8, "m2": uint8, "m3": uint8})

        expected_message = Baseline(
            """


            +--------+--------+-----------+-------+--------+
            | Offset | Access | Value     | Bytes | Format |
            +--------+--------+-----------+-------+--------+
            | 0      | ['m1'] | 0         | 00    | uint8  |
            |        | ['m2'] | (missing) |       | uint8  |
            |        | ['m3'] | (missing) |       | uint8  |
            +--------+--------+-----------+-------+--------+

            TypeError occurred during pack operation:

            missing values: 'm2', 'm3'
            """
        )

        assert str(trap.value) == expected_message

    def test_too_many_arg_value(self):
        """Test too many arg values present when simple DataMeta format."""
        expected_message = Baseline(
            """


            +--------+--------+-------+-------+--------------+
            | Offset | Access | Value | Bytes | Format       |
            +--------+--------+-------+-------+--------------+
            | 0      | [0]    | 0     | 00    | uint8        |
            | 1      | [1]    | 1     | 01    | uint8        |
            +--------+--------+-------+-------+--------------+
            |        | [2]    | 2     |       | (unexpected) |
            +--------+--------+-------+-------+--------------+

            TypeError occurred during pack operation:

            3 values given, expected 2
            """
        )

        with pytest.raises(PackError) as trap:
            pack((0, 1, 2), (uint8, uint8))

        assert str(trap.value) == expected_message

    def test_too_few_list_values(self):
        """Test too few list values present."""
        expected_message = Baseline(
            """


            +--------+--------+-----------+-------+-----------+
            | Offset | Access | Value     | Bytes | Format    |
            +--------+--------+-----------+-------+-----------+
            | 0      | [0]    | 0         | 00    | uint8     |
            |        | [1]    | (missing) |       | uint8     |
            |        | [2]    | (missing) |       | Structure |
            +--------+--------+-----------+-------+-----------+

            TypeError occurred during pack operation:

            1 value given, expected 3
            """
        )

        with pytest.raises(PackError) as trap:
            pack((0,), (uint8, uint8, Structure))

        assert str(trap.value) == expected_message

    def test_bad_format_type(self):
        """Test fmt is a type that doesn't support plum pack protocol."""
        expected_message = Baseline(
            """


            +--------+-------+-------+---------------+
            | Offset | Value | Bytes | Format        |
            +--------+-------+-------+---------------+
            |        | 0     |       | int (invalid) |
            +--------+-------+-------+---------------+

            TypeError occurred during pack operation:

            bad item format, must be a packable data type/transform (or a dict, list, or tuple of them)
            """
        )

        with pytest.raises(PackError) as trap:
            pack(0, int)

        assert str(trap.value) == expected_message

    def test_no_extras(self):
        """Test exception with no dump or embedded exception."""
        assert str(PackError("Hello.")) == "Hello."


class TestUnpackExceptions:

    """Test invalid format and value combinations when unpacking."""

    def test_bad_fmt(self):
        """Test fmt is an invalid type."""
        with pytest.raises(UnpackError) as trap:
            unpack(0, b"")

        expected_message = Baseline(
            """


            +--------+-------+-------+--------+
            | Offset | Value | Bytes | Format |
            +--------+-------+-------+--------+
            |        |       |       | 0      |
            +--------+-------+-------+--------+

            TypeError occurred during unpack operation:

            bad item format, must be a packable data type/transform (or a dict, list, or tuple of them)
            """
        )

        assert str(trap.value) == expected_message

    def test_bad_nested_fmt(self):
        """Test nested fmt is an invalid type."""
        with pytest.raises(UnpackError) as trap:
            unpack([0], b"")

        expected_message = Baseline(
            """


            +--------+--------+-------+-------+--------+
            | Offset | Access | Value | Bytes | Format |
            +--------+--------+-------+-------+--------+
            |        | [0]    |       |       | 0      |
            +--------+--------+-------+-------+--------+

            TypeError occurred during unpack operation:

            bad item format, must be a packable data type/transform (or a dict, list, or tuple of them)
            """
        )

        assert str(trap.value) == expected_message
