# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# Copyright 2021 Daniel Mark Gass, see __about__.py for license information.
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
"""Test "strict" feature (where strict=True)."""

import pytest

from baseline import Baseline

from plum.conformance import wrap_message
from plum.enum import EnumX
from plum.exceptions import PackError, UnpackError

from sample_enum import Register

register = EnumX("register", Register, 1, "big", signed=False)


class TestPack:

    """Test pack variants with invalid value."""

    expected_message = Baseline(
        """
        +--------+-------+-------+----------+
        | Offset | Value | Bytes | Format   |
        +--------+-------+-------+----------+
        |        | 4     |       | register |
        +--------+-------+-------+----------+

        ValueError occurred during pack operation:

        4 is not a valid Register
        """
    )

    def test_pack(self):
        with pytest.raises(PackError) as trap:
            register.pack(4)

        assert wrap_message(trap.value) == self.expected_message
        assert isinstance(trap.value.__context__, ValueError)

    def test_pack_and_dump(self):
        with pytest.raises(PackError) as trap:
            register.pack_and_dump(4)

        assert wrap_message(trap.value) == self.expected_message
        assert isinstance(trap.value.__context__, ValueError)


class TestUnpack:

    """Test unpack variants with invalid value."""

    expected_message = Baseline(
        """
        +--------+-------+-------+----------+
        | Offset | Value | Bytes | Format   |
        +--------+-------+-------+----------+
        | 0      | 4     | 04    | register |
        +--------+-------+-------+----------+

        ValueError occurred during unpack operation:

        4 is not a valid Register
        """
    )

    def test_unpack(self):
        with pytest.raises(UnpackError) as trap:
            register.unpack(b"\x04")

        assert wrap_message(trap.value) == self.expected_message
        assert isinstance(trap.value.__context__, ValueError)

    def test_unpack_and_dump(self):
        with pytest.raises(UnpackError) as trap:
            register.unpack_and_dump(b"\x04")

        assert wrap_message(trap.value) == self.expected_message
        assert isinstance(trap.value.__context__, ValueError)


class TestTransformCall:

    """Test transform call."""

    def test_call(self):
        expected_message = Baseline(
            """
            4 is not a valid Register
            """
        )
        with pytest.raises(ValueError) as trap:
            register(4)

        assert wrap_message(trap.value) == expected_message
