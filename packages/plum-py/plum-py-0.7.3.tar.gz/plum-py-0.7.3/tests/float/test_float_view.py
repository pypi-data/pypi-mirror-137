# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# Copyright 2021 Daniel Mark Gass, see __about__.py for license information.
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
"""Test float view to bytes buffer operations."""

from math import ceil, floor, trunc

import pytest
from baseline import Baseline

from plum.float import FloatX
from plum.utilities import pack

float32 = FloatX("float32", byteorder="big", nbytes=4)

# FUTURE: Rounding precision constant
# FUTURE: Clean up byte arrays


# pylint: disable=redefined-outer-name
@pytest.fixture()
def float32_view():
    """Sample float32 plum view."""
    buffer = b"\xff\x41\x45\x87\xe7\xff"
    yield float32.view(buffer, offset=1)  # float value of approx. 12.3456789


class TestFloatView:

    """Test operations float view to bytes buffer."""

    def test_arithmetic_assignments(self):
        """Test augmented arithmetic assignment operations."""
        buffer = bytearray([0xFF, 0x41, 0x45, 0x87, 0xE7, 0xFF])
        float32_view = float32.view(
            buffer, offset=1
        )  # float value of approx. 12.3456789

        # __iadd__
        float32_view += 1.234
        assert round(float32_view, 4) == round(13.579679489135742, 4)
        assert buffer == bytearray(b"\xffAYF^\xff")

        # __isub__
        float32_view -= 9.87654321
        assert round(float32_view, 4) == round(3.7031362791357427, 4)
        assert buffer == bytearray(b"\xff@m\x00/\xff")

        # __imul__
        float32_view *= 3.14159
        assert round(float32_view, 4) == round(11.633735656738281, 4)
        assert buffer == bytearray(b"\xffA:#\xc8\xff")

        # __imod__
        float32_view %= 2
        assert round(float32_view, 4) == round(1.6337356567382812, 4)
        assert buffer == bytearray(b"\xff?\xd1\x1e@\xff")

        # __ipow__
        float32_view **= 4
        assert round(float32_view, 4) == round(7.124053001403809, 4)
        assert buffer == bytearray(b"\xff@\xe3\xf8>\xff")

    def test_comparisons(self, float32_view):
        """Test comparison operations."""
        # pylint: disable=misplaced-comparison-constant

        # __lt__
        assert float32_view < 13.0
        assert not float32_view < 12.0

        # __le__
        assert float32_view <= 12.5
        assert not float32_view <= 12.25

        # __eq__
        assert float32_view == 12.34567928314209
        assert 12.34567928314209 == float32_view
        assert not float32_view == 98.67
        assert not 98.67 == float32_view

        # __ne__
        assert float32_view != 12.0
        assert 12.0 != float32_view

        # __gt__
        assert float32_view > 12.0
        assert not float32_view > 13.0

        # __ge__
        assert float32_view >= 12.25
        assert float32_view >= 12
        assert not float32_view >= 12.5
        assert not float32_view >= 13

    def test_numeric(self, float32_view):
        """Test comparison operations."""
        # __add__ and __radd__
        assert round(float32_view + 2, 4) == round(14.3456789, 4)
        assert round(2 + float32_view, 4) == round(14.3456789, 4)

        # __sub__ and __rsub__
        assert round(float32_view - 2, 4) == round(10.3456789, 4)
        assert round(20 - float32_view, 4) == round(7.6543211, 4)

        # __mul__ and __rmul__
        assert round(float32_view * 2, 4) == round(24.69135856628418, 4)
        assert round(2 * float32_view, 4) == round(24.69135856628418, 4)

        # __truediv__ and __rtruediv__
        assert round(float32_view / 3, 4) == round(4.11522642771403, 4)
        assert round(50 / float32_view, 4) == round(4.049999911165239, 4)

        # __mod__ and __rmod__
        assert round(float32_view % 5, 4) == round(2.34567928314209, 4)
        assert round(25.0 % float32_view, 4) == round(0.3086414337158203, 4)

        # __divmod__ and __rdivmod__
        assert divmod(float32_view, 3) == (4.0, 0.34567928314208984)
        assert divmod(24, float32_view) == (1.0, 11.65432071685791)

        # __pow__ and __rpow__
        assert round(float32_view**2, 4) == round(152.41579696220378, 4)
        assert round(2.0**float32_view, 4) == round(5204.988581065942, 4)

        # __ceil__ and __floor__
        assert ceil(float32_view) == 13
        assert floor(float32_view) == 12

        # __floordiv__ and __rfloordiv__
        assert float32_view // 2 == 6.0
        assert 30 // float32_view == 2.0

        # __round__ and __trunc__
        assert round(float32_view, 0) == 12
        assert trunc(float32_view) == 12

    def test_unary(self, float32_view):
        """Test unary operations."""
        assert round(-float32_view, 4) == round(-12.3456789, 4)  # __neg__
        assert round(+float32_view, 4) == round(12.3456789, 4)  # __pos__
        assert round(abs(float32_view), 4) == round(12.3456789, 4)  # __abs__
        assert int(float32_view) == 12  # __int__

    def test_pack_pos_argument(self, float32_view):
        """Test pack utility supports view as positional argument."""
        assert pack(float32_view, float32) == bytearray(b"AE\x87\xe7")

    def test_pack_kw_argument(self, float32_view):
        """Test pack utility supports view as keyword argument."""
        assert pack({"x": float32_view}, {"x": float32}) == bytearray(b"AE\x87\xe7")

    def test_unpack(self):
        """Test unpack() returns unpacked value."""
        buffer = bytearray(b"\xff\x41\x45\x87\xe7\xff")
        value = float32.view(buffer, offset=1).unpack()
        assert value == 12.34567928314209
        # changing buffer does not effect previously returned value
        buffer[0:6] = [0] * 6
        assert value == 12.34567928314209

    def test_set(self):
        """Test set()."""
        buffer = bytearray(6)
        float_view = float32.view(buffer, offset=1)
        assert float_view == 0.0
        float_view.set(12.34567928314209)
        assert float_view == 12.34567928314209
        assert buffer == bytearray([0x00, 0x41, 0x45, 0x87, 0xE7, 0x00])

    def test_representations(self, float32_view):
        """Test representations."""
        expected_dump = Baseline(
            """
                    +--------+-------------------+-------------+---------+
                    | Offset | Value             | Bytes       | Format  |
                    +--------+-------------------+-------------+---------+
                    | 1      | 12.34567928314209 | 41 45 87 e7 | float32 |
                    +--------+-------------------+-------------+---------+
                    """
        )

        assert str(float32_view) == "12.34567928314209"
        assert repr(float32_view) == "<view at 0x1: float32(12.34567928314209)>"
        assert str(float32_view.dump) == expected_dump
