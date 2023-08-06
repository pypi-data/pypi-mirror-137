# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# Copyright 2021 Daniel Mark Gass, see __about__.py for license information.
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
"""Test basic features of BitFields data store transform."""

# pylint: disable=invalid-name,unexpected-keyword-arg

import sys
from enum import IntEnum

import pytest
from baseline import Baseline

from plum.bitfields import BitFields, bitfield
from plum.conformance import wrap_message
from plum.enum import EnumX


class MyEnum(IntEnum):

    """Sample IntEnum."""

    A = 1
    B = 2


class TestInit:

    """Test constructor."""

    class MyBits(BitFields, nbytes=2, default=0x0):
        """Sample BitFields subclass."""

        f1: int = bitfield(lsb=0, size=8, default=0xAB)
        f2: MyEnum = bitfield(lsb=8, size=4)
        f3: bool = bitfield(lsb=12, size=1)
        f4: bool = bitfield(lsb=13, size=1)

    def test_invalid_arg_type(self):
        """Test invalid argument type passed to constructor."""
        expected_message = Baseline(
            """
            int() argument must be a string, a bytes-like object or a real number, not 'list'
            """
        )

        with pytest.raises(TypeError) as trap:
            self.MyBits(f1=[1], f2=0, f3=True, f4=True)

        actual_message = str(trap.value)

        if sys.version_info < (3, 10):
            actual_message = actual_message.replace("number", "real number")

        assert actual_message == expected_message


class TestInvalidInitValues:

    """Test out of range values passed to constructor."""

    class Struct(BitFields):
        f1 = bitfield(size=4, default=0)
        f2 = bitfield(size=4, signed=True, default=0)

    unsigned_message = Baseline(
        """
        bit field 'f1' requires 0 <= number <= 15
        """
    )

    signed_message = Baseline(
        """
        bit field 'f2' requires -8 <= number <= 7
        """
    )

    def test_too_small_for_signed(self):
        with pytest.raises(ValueError) as trap:
            self.Struct(f2=-9)

        assert wrap_message(trap.value) == self.signed_message

    def test_too_small_for_unsigned(self):
        with pytest.raises(ValueError) as trap:
            self.Struct(f1=-1)

        assert wrap_message(trap.value) == self.unsigned_message

    def test_too_big_for_signed(self):
        with pytest.raises(ValueError) as trap:
            self.Struct(f2=8)

        assert wrap_message(trap.value) == self.signed_message

    def test_too_big_for_unsigned(self):
        with pytest.raises(ValueError) as trap:
            self.Struct(f1=16)

        assert wrap_message(trap.value) == self.unsigned_message


class TestInvalidAttributeValues:

    """Test out of range attribute values."""

    class Struct(BitFields):
        f1 = bitfield(size=4, default=0)
        f2 = bitfield(size=4, signed=True, default=0)

    unsigned_message = Baseline(
        """
        bit field 'f1' requires 0 <= number <= 15
        """
    )

    signed_message = Baseline(
        """
        bit field 'f2' requires -8 <= number <= 7
        """
    )

    def test_too_small_for_signed(self):
        with pytest.raises(ValueError) as trap:
            self.Struct().f2 = -9

        assert wrap_message(trap.value) == self.signed_message

    def test_too_small_for_unsigned(self):
        with pytest.raises(ValueError) as trap:
            self.Struct().f1 = -1

        assert wrap_message(trap.value) == self.unsigned_message

    def test_too_big_for_signed(self):
        with pytest.raises(ValueError) as trap:
            self.Struct().f2 = 8

        assert wrap_message(trap.value) == self.signed_message

    def test_too_big_for_unsigned(self):
        with pytest.raises(ValueError) as trap:
            self.Struct().f1 = 16

        assert wrap_message(trap.value) == self.unsigned_message


class ForCompare(BitFields, nbytes=1, default=0x0, ignore=0xC0):

    """Sample BitFields subclass with ignored fields."""

    f1: int = bitfield(lsb=0, size=4)
    f2: int = bitfield(lsb=4, size=2, ignore=True)
    f3: int = bitfield(lsb=6, size=2)  # gets ignored from class 'ignore'


class TestEquality:

    """Test __eq__ and __ne__ operators.

    Test common normalization algorithms that implement ignore mechanisms.
    Rely on TestCompares to thoroughly check support for each of the other
    comparison methods (e.g. __le__, __lt__, etc.).

    """

    # pylint: disable=unneeded-not

    def test_int(self):
        """Verify when other is int, nothing ignored"""
        assert ForCompare(f1=1, f2=2, f3=2) == 0xA1

    def test_ignore_field(self):
        """Verify when other is same type as self, field marked as ignore doesn't matter."""
        assert ForCompare(f1=1, f2=2, f3=2) == ForCompare(f1=1, f2=0, f3=2)
        assert not ForCompare(f1=0, f2=2, f3=2) == ForCompare(f1=1, f2=2, f3=2)

    def test_ignore_mask(self):
        """Verify when other is same type as self, subclass ignore mask applies."""
        assert ForCompare(f1=1, f2=2, f3=2) == ForCompare(f1=1, f2=2, f3=3)
        assert not ForCompare(f1=0, f2=2, f3=2) == ForCompare(f1=1, f2=2, f3=2)


class TestCompares:

    """Verify comparison operators.

    Assume all operators implemented with a common normalization
    algorithm. Only spot check each operator and rely on TestEquality
    test cases to validate the common normalization algorithm.

    """

    # pylint: disable=unneeded-not

    def test_lt(self):
        """Spot check 'lt' operator."""
        assert ForCompare(f1=1, f2=2, f3=2) < 0xA2
        assert not ForCompare(f1=1, f2=2, f3=2) < 0xA0

    def test_le(self):
        """Spot check 'lt' operator."""
        assert ForCompare(f1=1, f2=2, f3=2) <= 0xA1
        assert not ForCompare(f1=1, f2=2, f3=2) <= 0xA0

    def test_eq(self):
        """Spot check 'eq' operator."""
        assert ForCompare(f1=1, f2=2, f3=2) == 0xA1
        assert not ForCompare(f1=1, f2=2, f3=2) == 0xA0

    def test_ne(self):
        """Spot check 'ne' operator."""
        assert ForCompare(f1=1, f2=2, f3=2) != 0xA0
        assert not ForCompare(f1=1, f2=2, f3=2) != 0xA1

    def test_gt(self):
        """Spot check 'gt' operator."""
        assert ForCompare(f1=1, f2=2, f3=2) > 0xA0
        assert not ForCompare(f1=1, f2=2, f3=2) > 0xA2

    def test_ge(self):
        """Spot check 'ge' operator."""
        assert ForCompare(f1=1, f2=2, f3=2) >= 0xA1
        assert not ForCompare(f1=1, f2=2, f3=2) >= 0xA2


class SimpleBits(BitFields, nbytes=1):

    """Sample BitFields subclass."""

    f1: int = bitfield(lsb=0, size=8, default=0)


class TestArithmetic:

    """Verify arithmetic operators.

    Assume all operators implemented with a common normalization
    algorithm. Only spot check each operator.

    """

    # pylint: disable=unidiomatic-typecheck,too-many-public-methods

    def test_add(self):
        """Spot check '+' operator."""
        x = SimpleBits.from_int(0) + 1
        assert x == 1
        assert type(x) is int

    def test_sub(self):
        """Spot check '-' operator."""
        x = SimpleBits.from_int(3) - 1
        assert x == 2
        assert type(x) is int

    def test_mul(self):
        """Spot check '*' operator."""
        x = SimpleBits.from_int(3) * 4
        assert x == 12
        assert type(x) is int

    def test_truediv(self):
        """Spot check '/' operator."""
        x = SimpleBits.from_int(9) / 2
        assert x == 4.5
        assert type(x) is float

    def test_floordiv(self):
        """Spot check '//' operator."""
        x = SimpleBits.from_int(9) // 2
        assert x == 4
        assert type(x) is int

    def test_mod(self):
        """Spot check '%' operator."""
        x = SimpleBits.from_int(9) % 2
        assert x == 1
        assert type(x) is int

    def test_divmod(self):
        """Spot check divmod() operator."""
        div, mod = divmod(SimpleBits.from_int(9), 2)
        assert div == 4
        assert mod == 1
        assert type(div) is int
        assert type(mod) is int

    def test_pow(self):
        """Spot check '**' operator."""
        x = SimpleBits.from_int(2) ** 3
        assert x == 8
        assert type(x) is int

        x = pow(SimpleBits.from_int(2), 3, 5)
        assert x == 3
        assert type(x) is int

    def test_radd(self):
        """Spot check '+' operator (right hand size)."""
        x = 1 + SimpleBits.from_int(0)
        assert x == 1
        assert type(x) is int

    def test_rsub(self):
        """Spot check '-' operator (right hand size)."""
        x = 3 - SimpleBits.from_int(1)
        assert x == 2
        assert type(x) is int

    def test_rmul(self):
        """Spot check '*' operator (right hand size)."""
        x = 4 * SimpleBits.from_int(3)
        assert x == 12
        assert type(x) is int

    def test_rtruediv(self):
        """Spot check '/' operator (right hand size)."""
        x = 9 / SimpleBits.from_int(2)
        assert x == 4.5
        assert type(x) is float

    def test_rfloordiv(self):
        """Spot check '//' operator (right hand size)."""
        x = 9 // SimpleBits.from_int(2)
        assert x == 4
        assert type(x) is int

    def test_rmod(self):
        """Spot check '%' operator (right hand size)."""
        x = 9 % SimpleBits.from_int(2)
        assert x == 1
        assert type(x) is int

    def test_rdivmod(self):
        """Spot check divmod() operator (right hand size)."""
        div, mod = divmod(9, SimpleBits.from_int(2))
        assert div == 4
        assert mod == 1
        assert type(div) is int
        assert type(mod) is int

    def test_rpow(self):
        """Spot check '**' operator (right hand size)."""
        x = 2 ** SimpleBits.from_int(3)
        assert x == 8
        assert type(x) is int

        # Note, Python does not support this:
        # x = pow(2, SimpleBits.from_int(3), 5)
        # assert x == 3
        # assert type(x) is int

    def test_iadd(self):
        """Spot check '+' operator (in place)."""
        x = SimpleBits.from_int(0)
        x += 1
        assert x == 1
        assert type(x) is int

    def test_isub(self):
        """Spot check '-' operator (in place)."""
        x = SimpleBits.from_int(3)
        x -= 1
        assert x == 2
        assert type(x) is int

    def test_imul(self):
        """Spot check '*' operator (in place)."""
        x = SimpleBits.from_int(3)
        x *= 4
        assert x == 12
        assert type(x) is int

    def test_itruediv(self):
        """Spot check '/' operator (in place)."""
        x = SimpleBits.from_int(9)
        x /= 2
        assert x == 4.5
        assert type(x) is float

    def test_ifloordiv(self):
        """Spot check '//' operator (in place)."""
        x = SimpleBits.from_int(9)
        x //= 2
        assert x == 4
        assert type(x) is int

    def test_imod(self):
        """Spot check '%' operator (in place)."""
        x = SimpleBits.from_int(9)
        x %= 2
        assert x == 1
        assert type(x) is int

    def test_neg(self):
        """Spot check neg() operator."""
        x = -SimpleBits.from_int(9)  # pylint: disable=invalid-unary-operand-type
        assert x == -9
        assert type(x) is int

    def test_pos(self):
        """Spot check neg() operator."""
        x = +SimpleBits.from_int(9)  # pylint: disable=invalid-unary-operand-type
        assert x == 9
        assert type(x) is int

    def test_abs(self):
        """Spot check abs() operator."""
        x = abs(SimpleBits.from_int(9))
        assert x == 9
        assert type(x) is int

    def test_invert(self):
        """Spot check '~' operator."""
        x = ~SimpleBits.from_int(1)  # pylint: disable=invalid-unary-operand-type
        assert x == -2
        assert type(x) is int

    def test_float(self):
        """Spot check float() operator."""
        x = float(SimpleBits.from_int(9))
        assert x == 9.0

    def test_index(self):
        """Spot check __index__ method."""
        numbers = list(range(10))
        # pylint: disable=invalid-sequence-index
        assert numbers[SimpleBits.from_int(1)] == numbers[1]

    def test_round(self):
        """Spot check round() support."""
        x = round(SimpleBits.from_int(1))
        assert x == 1
        assert type(x) is int


class TestBitLogic:
    """Verify bit shift and logical operators.

    Assume all operators implemented with a common normalization
    algorithm. Only spot check each operator.

    """

    # pylint: disable=unidiomatic-typecheck

    def test_lshift(self):
        """Spot check '<<' operator."""
        x = SimpleBits.from_int(1) << 2
        assert x == 1 << 2
        assert type(x) is int

    def test_rshift(self):
        """Spot check '>>' operator."""
        x = SimpleBits.from_int(1 << 2) >> 2
        assert x == 1
        assert type(x) is int

    def test_and(self):
        """Spot check '&' operator."""
        x = SimpleBits.from_int(3) & 2
        assert x == 2
        assert type(x) is int

    def test_xor(self):
        """Spot check '^' operator."""
        x = SimpleBits.from_int(0b1010) ^ 0b1100
        assert x == 0b0110
        assert type(x) is int

    def test_or(self):
        """Spot check '|' operator."""
        x = SimpleBits.from_int(0b010) | 0b001
        assert x == 0b011
        assert type(x) is int

    def test_rlshift(self):
        """Spot check '<<' operator (right hand size)."""
        x = 1 << SimpleBits.from_int(2)
        assert x == 1 << 2
        assert type(x) is int

    def test_rrshift(self):
        """Spot check '>>' operator (right hand size)."""
        x = (1 << 2) >> SimpleBits.from_int(2)
        assert x == 1
        assert type(x) is int

    def test_rand(self):
        """Spot check '&' operator (right hand size)."""
        x = 2 & SimpleBits.from_int(3)
        assert x == 2
        assert type(x) is int

    def test_rxor(self):
        """Spot check '^' operator (right hand size)."""
        x = 0b1100 ^ SimpleBits.from_int(0b1010)
        assert x == 0b0110
        assert type(x) is int

    def test_ror(self):
        """Spot check '|' operator (right hand size)."""
        x = 0b001 | SimpleBits.from_int(0b010)
        assert x == 0b011
        assert type(x) is int

    def test_ilshift(self):
        """Spot check '<<' operator (in place)."""
        x = SimpleBits.from_int(1)
        x <<= 2
        assert x == 1 << 2
        assert type(x) is int

    def test_irshift(self):
        """Spot check '>>' operator (in place)."""
        x = SimpleBits.from_int(1 << 2)
        x >>= 2
        assert x == 1
        assert type(x) is int

    def test_iand(self):
        """Spot check '&' operator (in place)."""
        x = SimpleBits.from_int(3)
        x &= 2
        assert x == 2
        assert type(x) is int

    def test_ixor(self):
        """Spot check '^' operator (in place)."""
        x = SimpleBits.from_int(0b1010)
        x ^= 0b1100
        assert x == 0b0110
        assert type(x) is int

    def test_ior(self):
        """Spot check '|' operator (in place)."""
        x = SimpleBits.from_int(0b010)
        x |= 0b001
        assert x == 0b011
        assert type(x) is int


class TestHash:

    """Test support of hash()."""

    def test_hash(self):
        """Verify hash does not include ignored fields."""
        assert hash(ForCompare(f1=1, f2=1, f3=1)) == hash(1)


class TestBool:

    """Test conversion with bool()."""

    def test_bool(self):
        """Verify bool does not consider ignored fields."""
        assert ForCompare(f1=1, f2=0, f3=0)
        assert not ForCompare(f1=0, f2=1, f3=1)


class ForSigned(BitFields, nbytes=1):

    """Sample BitFields subclass with signed field."""

    f1: int = bitfield(lsb=0, size=2)
    f2: int = bitfield(lsb=2, size=4, signed=True)
    f3: int = bitfield(lsb=6, size=2)


class TestSigned:

    """Test signed BitField member."""

    def test_get(self):
        """Verify get access."""
        assert ForSigned.from_int(0xC3).f2 == 0
        assert ForSigned.from_int(0x3C).f2 == -1
        assert ForSigned.from_int(0xE3).f2 == -8

    def test_valid_set(self):
        """Verify set access."""
        bitfields = ForSigned.from_int(0)
        bitfields.f2 = -1
        assert int(bitfields) == 0x3C

        bitfields = ForSigned.from_int(0)
        bitfields.f2 = 7
        assert int(bitfields) == 0x1C

        bitfields = ForSigned.from_int(0xC3)
        bitfields.f2 = -8
        assert int(bitfields) == 0xE3

        bitfields = ForSigned.from_int(0xFF)
        bitfields.f2 = 0
        assert int(bitfields) == 0xC3

    def test_invalid_set(self):
        """Test value out of range."""
        expected = Baseline(
            """
            bit field 'f2' requires -8 <= number <= 7
            """
        )

        bitfields = ForSigned.from_int(0)

        with pytest.raises(ValueError) as trap:
            bitfields.f2 = 8
        assert wrap_message(trap.value) == expected

        with pytest.raises(ValueError) as trap:
            bitfields.f2 = -9
        assert wrap_message(trap.value) == expected


class ForUnsigned(BitFields, nbytes=1):

    """Sample BitFields subclass with signed field."""

    f1: int = bitfield(lsb=0, size=2)
    f2: int = bitfield(lsb=2, size=4)
    f3: int = bitfield(lsb=6, size=2)


class TestUnsigned:

    """Test unsigned bit field member."""

    def test_get(self):
        """Verify get access."""
        assert ForUnsigned.from_int(0xC3).f2 == 0
        assert ForUnsigned.from_int(0xC7).f2 == 1
        assert ForUnsigned.from_int(0xE3).f2 == 8
        assert ForUnsigned.from_int(0x3C).f2 == 0xF

    def test_valid_set(self):
        """Verify set access."""
        bitfields = ForUnsigned.from_int(0)
        bitfields.f2 = 0xF
        assert int(bitfields) == 0x3C

        bitfields = ForUnsigned.from_int(0xFF)
        bitfields.f2 = 0
        assert int(bitfields) == 0xC3

        bitfields = ForUnsigned.from_int(0x0)
        bitfields.f2 = 1
        assert int(bitfields) == 4

        bitfields = ForUnsigned.from_int(0x0)
        bitfields.f2 = 8
        assert int(bitfields) == 0x20

    def test_invalid_set(self):
        """Test value out of range."""
        expected = Baseline(
            """
            bit field 'f2' requires 0 <= number <= 15
            """
        )

        bitfields = ForUnsigned.from_int(0)

        with pytest.raises(ValueError) as trap:
            bitfields.f2 = -1
        assert wrap_message(trap.value) == expected

        with pytest.raises(ValueError) as trap:
            bitfields.f2 = 16
        assert wrap_message(trap.value) == expected


class ForStrictEnum(BitFields, nbytes=1):

    """Sample BitFields subclass with enumeration field."""

    f1: int = bitfield(lsb=0, size=2)
    f2: MyEnum = bitfield(lsb=2, size=4, typ=MyEnum)
    f3: int = bitfield(lsb=6, size=2)


class TestStrictEnum:

    """Test enumeration bit field member."""

    def test_happy_get(self):
        """Verify get access succeeds with valid value."""
        assert ForStrictEnum.from_int(1 << 2).f2 is MyEnum.A

    def test_unhappy_get(self):
        """Verify get access fails when invalid value."""

        expected_message = Baseline(
            """
            0 is not a valid MyEnum
            """
        )

        with pytest.raises(ValueError) as trap:
            # pylint: disable=expression-not-assigned
            ForStrictEnum.from_int(0).f2

        assert str(trap.value) == expected_message

    def test_happy_set(self):
        """Verify set access succeeds with valid value."""
        bitfields = ForStrictEnum.from_int(0)
        bitfields.f2 = MyEnum.A
        assert int(bitfields) == 1 << 2

    def test_unhappy_set(self):
        """Verify set access fails with invalid value."""
        expected_message = Baseline(
            """
            0 is not a valid MyEnum
            """
        )

        bitfields = ForStrictEnum.from_int(0)

        with pytest.raises(ValueError) as trap:
            bitfields.f2 = 0

        assert str(trap.value) == expected_message


class ForTolerantEnum(BitFields, nbytes=1):

    """Sample BitFields subclass with enumeration field."""

    f1: int = bitfield(lsb=0, size=2)
    f2: int = bitfield(lsb=2, size=4, typ=EnumX("myenum", MyEnum, strict=False))
    f3: int = bitfield(lsb=6, size=2)


class TestTolerantEnum:
    """Test enumeration bit field member."""

    def test_happy_get(self):
        """Verify get access succeeds with valid value."""
        assert ForTolerantEnum.from_int(1 << 2).f2 is MyEnum.A

    def test_tolerant_get(self):
        """Verify get access fails when invalid value."""
        assert ForTolerantEnum.from_int(0).f2 == 0

    def test_happy_set(self):
        """Verify set access succeeds with valid value."""
        bitfields = ForTolerantEnum.from_int(0)
        bitfields.f2 = MyEnum.A
        assert int(bitfields) == 1 << 2

    def test_tolerant_set(self):
        """Verify set access fails with invalid value."""
        bitfields = ForTolerantEnum.from_int(0)
        bitfields.f2 = 3
        assert int(bitfields) == 3 << 2


class TestAsDict:

    """Test asdict() method."""

    class MyBits(BitFields):
        """Sample BitFields subclass."""

        f1 = bitfield(size=4)
        f2 = bitfield(size=4)

    def test_method(self):
        sample = self.MyBits(f1=1, f2=2)

        assert sample.asdict() == {"f1": 1, "f2": 2}
