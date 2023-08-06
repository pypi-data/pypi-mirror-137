# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# Copyright 2021 Daniel Mark Gass, see __about__.py for license information.
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
"""Test "strict" feature (where strict=False)."""

# pylint: disable=unidiomatic-typecheck

from baseline import Baseline

from plum.enum import EnumX

from sample_enum import Register

register = EnumX("register", Register, 1, "big", signed=False, strict=False)


class TestPack:

    """Test pack variants with invalid value."""

    expected_dump = Baseline(
        """
        +--------+-------+-------+----------+
        | Offset | Value | Bytes | Format   |
        +--------+-------+-------+----------+
        | 0      | 4     | 04    | register |
        +--------+-------+-------+----------+
        """
    )

    def test_pack(self):
        assert register.pack(4) == b"\x04"

    def test_pack_and_dump(self):
        buffer, dump = register.pack_and_dump(4)
        assert buffer == b"\x04"
        assert str(dump) == self.expected_dump


class TestUnpack:

    """Test unpack variants with invalid value."""

    expected_dump = Baseline(
        """
        +--------+-------+-------+----------+
        | Offset | Value | Bytes | Format   |
        +--------+-------+-------+----------+
        | 0      | 4     | 04    | register |
        +--------+-------+-------+----------+
        """
    )

    def test_unpack(self):
        value = register.unpack(b"\x04")
        assert value == 4
        assert type(value) is int

    def test_unpack_and_dump(self):
        value, dump = register.unpack_and_dump(b"\x04")
        assert str(dump) == self.expected_dump
        assert value == 4
        assert type(value) is int


class TestTransformCall:

    """Test transform call."""

    def test_call(self):
        assert register(4) == 4
        assert type(register(4)) is int
