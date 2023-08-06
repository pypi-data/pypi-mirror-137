# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# Copyright 2021 Daniel Mark Gass, see __about__.py for license information.
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
"""Test operations int view of buffer bytes."""

from math import ceil, floor, trunc

import pytest
from baseline import Baseline

from plum.bigendian import uint8, uint16
from plum.conformance import wrap_message
from plum.utilities import pack


# pylint: disable=redefined-outer-name
@pytest.fixture()
def uint8_view():
    """Sample uint8 plum view."""
    buffer = b"\x01\x02\x0A\x0B"
    yield uint8.view(buffer, offset=2)  # decimal value of 10


class TestIntView:

    """Test operations int view of buffer bytes."""

    def test_arithmetic_assignments(self):
        """Test augmented arithmetic assignment operations."""
        memory_backing = bytearray([0x00, 0x01, 0x04, 0xFF])
        uint16_view = uint16.view(memory_backing, offset=1)  # decimal value of 260

        # __iadd__
        uint16_view += 8
        assert uint16_view == 268
        assert memory_backing == bytearray(b"\x00\x01\x0c\xff")

        # __isub__
        uint16_view -= 204
        assert uint16_view == 64
        assert memory_backing == bytearray(b"\x00\x00\x40\xff")

        # __imul__
        uint16_view *= 16
        assert uint16_view == 1024
        assert memory_backing == bytearray(b"\x00\x04\x00\xff")

        # __imod__
        uint16_view %= 306
        assert uint16_view == 106
        assert memory_backing == bytearray(b"\x00\x00\x6a\xff")

        # __ipow__
        uint16_view **= 2
        assert uint16_view == 11236
        assert memory_backing == bytearray(b"\x00\x2b\xe4\xff")

        # __ilshift__
        uint16_view <<= 1
        assert uint16_view == 22472
        assert memory_backing == bytearray(b"\x00\x57\xc8\xff")

        # __irshift__
        uint16_view >>= 8
        assert uint16_view == 87
        assert memory_backing == bytearray(b"\x00\x00\x57\xff")

        # __ixor__
        uint16_view ^= 0x0F0F
        assert uint16_view == 3928
        assert memory_backing == bytearray(b"\x00\x0f\x58\xff")

        # __iand__
        uint16_view &= 0xFF08
        assert uint16_view == 3848
        assert memory_backing == bytearray(b"\x00\x0f\x08\xff")

        # __ior__
        uint16_view |= 0xA0F0
        assert uint16_view == 45048
        assert memory_backing == bytearray(b"\x00\xaf\xf8\xff")

    def test_bitwise(self, uint8_view):
        """Test bitwise operations."""
        # __lshift__ and __rlshift__
        assert uint8_view << 2 == 40
        assert 2 << uint8_view == 2048

        # __rshift__ and __rrshift__
        assert uint8_view >> 1 == 5
        assert 4096 >> uint8_view == 4

        # __and__ and __rand__
        assert uint8_view & 3 == 2
        assert 12 & uint8_view == 8

        # __xor__ and __rxor__
        assert uint8_view ^ 8 == 2
        assert 14 ^ uint8_view == 4

        # __or__ and __ror__
        assert uint8_view | 7 == 15
        assert 3 | uint8_view == 11

    def test_comparisons(self, uint8_view):
        """Test comparison operations."""
        # __lt__
        assert uint8_view < 12
        assert not uint8_view < 8

        # __le__
        assert uint8_view <= 12
        assert uint8_view <= 10
        assert not uint8_view <= 4

        # __eq__
        assert uint8_view == 10
        assert 10 == uint8_view  # pylint: disable=misplaced-comparison-constant
        assert not uint8_view == 18
        assert not 18 == uint8_view  # pylint: disable=misplaced-comparison-constant

        # __ne__
        assert uint8_view != 20
        assert 20 != uint8_view  # pylint: disable=misplaced-comparison-constant
        assert not uint8_view != 10
        assert not 10 != uint8_view  # pylint: disable=misplaced-comparison-constant

        # __gt__
        assert uint8_view > 2
        assert not uint8_view > 16

        # __ge__
        assert uint8_view >= 10
        assert uint8_view >= 9
        assert not uint8_view >= 11

    def test_conversions(self, uint8_view):
        """Test type conversion operations."""
        assert str(uint8_view) == "10"
        assert float(uint8_view) == 10.0

    def test_numeric(self, uint8_view):
        """Test comparison operations."""
        # __add__ and __radd__
        assert uint8_view + 2 == 12
        assert 2 + uint8_view == 12

        # __sub__ and __rsub__
        assert uint8_view - 4 == 6
        assert 24 - uint8_view == 14

        # __mul__ and __rmul__
        assert uint8_view * 4 == 40
        assert 6 * uint8_view == 60

        # __truediv__ and __rtruediv__
        assert uint8_view / 2 == 5
        assert 30 / uint8_view == 3

        # __mod__ and __rmod__
        assert uint8_view % 6 == 4
        assert 48 % uint8_view == 8

        # __divmod__ and __rdivmod__
        assert divmod(uint8_view, 3) == (3, 1)
        assert divmod(24, uint8_view) == (2, 4)

        # __pow__ and __rpow__
        assert uint8_view**3 == 1000
        assert 2**uint8_view == 1024

        # __ceil__ and __floor__
        assert ceil(uint8_view) == 10
        assert floor(uint8_view) == 10

        # __floordiv__ and __rfloordiv__
        assert uint8_view // 2 == 5
        assert 20 // uint8_view == 2

        # __round__ and __trunc__
        assert round(uint8_view, 0) == 10
        assert trunc(uint8_view) == 10

    def test_unary(self, uint8_view):
        """Test unary operations."""
        assert -uint8_view == -10  # __neg__
        assert +uint8_view == 10  # __pos__
        assert abs(uint8_view) == 10  # __abs__
        assert int(uint8_view) == 10  # __int__
        assert ~uint8_view == -11  # __invert__

    def test_pack_pos_argument(self, uint8_view):
        """Test pack() utility supports view as positional argument."""
        assert pack(uint8_view, uint8) == bytearray(b"\x0a")

    def test_pack_kw_argument(self, uint8_view):
        """Test pack() utility supports view as keyword argument."""
        assert pack({"x": uint8_view}, {"x": uint8}) == bytearray(b"\x0a")

    def test_unpack(self):
        """Test unpack() returns unpacked value."""
        buffer = bytearray(b"\x01\x02\x0A\x0B")
        value = uint8.view(buffer, offset=2).unpack()
        assert value == 10
        # changing buffer does not effect previously returned value
        buffer[0:4] = [0] * 4
        assert value == 10

    def test_set(self):
        """Test set()."""
        buffer = bytearray(4)
        int_view = uint8.view(buffer, offset=2)
        assert int_view == 0
        int_view.set(1)
        assert int_view == 1
        assert buffer == bytearray([0x00, 0x00, 0x01, 0x00])

    def test_representations(self, uint8_view):
        """Test representations."""
        expected_dump = Baseline(
            """
                    +--------+-------+-------+--------+
                    | Offset | Value | Bytes | Format |
                    +--------+-------+-------+--------+
                    | 2      | 10    | 0a    | uint8  |
                    +--------+-------+-------+--------+
                    """
        )

        assert str(uint8_view) == "10"
        assert repr(uint8_view) == "<view at 0x2: uint8(10)>"
        assert str(uint8_view.dump) == expected_dump

    def test_dereference(self, uint8_view):
        """Test dereference operation exception."""

        with pytest.raises(RuntimeError) as trap:
            uint8_view[0]  # pylint: disable=pointless-statement

        expected = Baseline(
            """
            <transform 'uint8'> type does not support pointer dereference
            """
        )

        assert wrap_message(trap.value) == expected
