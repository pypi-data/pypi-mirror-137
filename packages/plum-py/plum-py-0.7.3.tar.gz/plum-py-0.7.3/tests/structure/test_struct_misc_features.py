# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# Copyright 2021 Daniel Mark Gass, see __about__.py for license information.
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
"""Test Structure type features."""

from enum import IntEnum

import pytest
from baseline import Baseline

from plum.conformance import wrap_message
from plum.enum import EnumX
from plum.exceptions import PackError
from plum.littleendian import uint8, uint16
from plum.structure import Structure, bitfield_member, member
from plum.utilities import pack


class Custom(Structure):

    """Sample structure type."""

    mbr1: int = member(fmt=uint8)
    mbr2: int = member(fmt=uint16, default=0x9988)


sample_dump = Baseline(
    """
    +--------+--------+-------+-------+--------+
    | Offset | Access | Value | Bytes | Format |
    +--------+--------+-------+-------+--------+
    |        |        |       |       | Custom |
    | 0      | mbr1   | 1     | 01    | uint8  |
    | 1      | mbr2   | 2     | 02 00 | uint16 |
    +--------+--------+-------+-------+--------+
    """
)


class TestInit:

    """Test initializer."""

    @staticmethod
    def test_init_keyword():
        """Test initialization via keyword arguments (no defaults)."""
        custom = Custom(mbr1=1, mbr2=2)
        assert str(custom.dump) == sample_dump

    @staticmethod
    def test_init_keyword_default():
        """Test initialization via keyword arguments (use defaults)."""
        custom = Custom(mbr1=1)

        expected_dump = Baseline(
            """
            +--------+--------+-------+-------+--------+
            | Offset | Access | Value | Bytes | Format |
            +--------+--------+-------+-------+--------+
            |        |        |       |       | Custom |
            | 0      | mbr1   | 1     | 01    | uint8  |
            | 1      | mbr2   | 39304 | 88 99 | uint16 |
            +--------+--------+-------+-------+--------+
            """
        )

        assert str(custom.dump) == expected_dump


class TestIndexAccess:

    """Test __setitem__ and __getitem__ usages."""

    sample = Custom(mbr1=1, mbr2=2)
    sample_dump = sample_dump

    def test_valid_lookup(self):
        """Test __getitem__ with valid index."""
        assert self.sample[0] == 1
        assert self.sample[1] == 2

    def test_valid_set(self):
        """Test __setitem__ with valid index."""
        cls = type(self.sample)
        sample = cls(mbr1=0, mbr2=2)
        sample[0] = 1
        assert str(sample.dump) == self.sample_dump

    def test_valid_slice_set(self):
        """Test __setitem__ with valid slice index."""
        cls = type(self.sample)
        sample = cls(mbr1=11, mbr2=22)
        sample[0:2] = [1, 2]
        assert str(sample.dump) == self.sample_dump

    def test_invalid_lookup(self):
        """Test __getitem__ with out of range index."""
        with pytest.raises(IndexError) as trap:
            # pylint: disable=pointless-statement
            self.sample[2]

        assert str(trap.value) == "list index out of range"

    def test_invalid_set_index(self):
        """Test __setitem__ with out of range index."""
        with pytest.raises(IndexError) as trap:
            self.sample[2] = 2

        assert str(trap.value) == "list assignment index out of range"


class TestNameAccess:

    """Test member access via attribute."""

    sample = Custom(mbr1=1, mbr2=2)
    sample_dump = sample_dump

    # pylint: disable=unneeded-not

    def test_valid_lookup(self):
        """Test member get via attribute access with valid name."""
        assert self.sample.mbr1 == 1
        assert self.sample.mbr2 == 2

    def test_valid_set(self):
        """Test member set via attribute access with valid name."""
        sample = Custom(mbr1=0, mbr2=2)
        sample.mbr1 = 1
        assert str(sample.dump) == self.sample_dump

    def test_invalid_lookup(self):
        """Test member get via attribute access with invalid name."""
        with pytest.raises(AttributeError) as trap:
            # pylint: disable=no-member,pointless-statement
            self.sample.m3

        clsname = type(self.sample).__name__
        assert str(trap.value) == f"{clsname!r} object has no attribute 'm3'"

    def test_invalid_set(self):
        """Test member set via attribute access with valid name."""
        cls = type(self.sample)
        sample = cls(mbr1=0, mbr2=2)
        with pytest.raises(AttributeError) as trap:
            sample.m3 = 0

        assert str(trap.value) == f"{cls.__name__!r} object has no attribute 'm3'"


class Sample(Structure):

    """Sample structure type."""

    mbr1: int = member(fmt=uint8)
    mbr2: int = member(fmt=uint8)


class TestExceptions:

    """Test exception corner cases."""

    def test_member_duplicate(self):
        """Test member definition may only be used once in one structure class."""

        expected = Baseline(
            """
            invalid structure member 'xyz' definition, member instance can not be
            shared, create a new instance
            """
        )

        with pytest.raises(TypeError) as trap:

            class Struct(Structure):  # pylint: disable=unused-variable

                abc = member(fmt=uint8)
                xyz = abc

        assert wrap_message(trap.value) == expected

    def test_member_already_in_use(self):
        """Test member definition may only be used in one structure class."""

        expected = Baseline(
            """
            invalid structure member 'xyz' definition, member instance can not be
            shared, create a new instance
            """
        )

        memb = member(fmt=uint8)

        class FirstUse(Structure):  # pylint: disable=unused-variable

            xyz = memb

        with pytest.raises(TypeError) as trap:

            class SecondUse(Structure):  # pylint: disable=unused-variable

                xyz = memb

        assert wrap_message(trap.value) == expected

    def test_invalid_fieldorder(self):
        expected = Baseline(
            """
            fieldorder must be either "least_to_most" or "most_to_least"
            """
        )

        with pytest.raises(ValueError) as trap:

            class Struct(
                Structure, fieldorder="invalid"
            ):  # pylint: disable=unused-variable
                pass

        assert wrap_message(trap.value) == expected

    def test_bitfield_already_in_use(self):
        """Test bitfield member definition may only be used in one structure class."""

        expected = Baseline(
            """
            invalid structure member 'xyz' definition, member instance can not be
            shared, create a new instance
            """
        )

        bitfield = bitfield_member(typ=int, lsb=0, size=1)

        class FirstUse(Structure):  # pylint: disable=unused-variable

            xyz = bitfield

        with pytest.raises(TypeError) as trap:

            class SecondUse(Structure):  # pylint: disable=unused-variable

                xyz = bitfield

        assert wrap_message(trap.value) == expected

    def test_invalid_member_type(self):
        """Test member type not a plum type."""
        with pytest.raises(TypeError) as trap:

            class Bad(Structure):  # pylint: disable=unused-variable
                """Sample structure with member with invalid type."""

                m1: int = member(fmt=int)

        exp_message = Baseline(
            """
            'fmt' must be a data store, transform, or a factory function
            """
        )

        assert str(trap.value) == exp_message

    def test_defined_struct_pack_bad_value(self):
        """Test value to predefined structure pack is not an iterable of members."""
        exp_message = Baseline(
            """
             +--------+-------+-------+--------+
             | Offset | Value | Bytes | Format |
             +--------+-------+-------+--------+
             |        |       |       | Custom |
             +--------+-------+-------+--------+

             TypeError occurred during pack operation:

             cannot unpack non-iterable int object
             """
        )

        with pytest.raises(PackError) as trap:
            pack(0, Custom)

        assert wrap_message(trap.value) == exp_message
        assert isinstance(trap.value.__context__, TypeError)

    def test_pack_value_missing_member(self):
        """Test tuple value to pack is missing a required member."""
        with pytest.raises(PackError) as trap:
            pack((0,), Sample)

        exp_message = Baseline(
            """
             +--------+-------+-------+--------+
             | Offset | Value | Bytes | Format |
             +--------+-------+-------+--------+
             |        |       |       | Sample |
             +--------+-------+-------+--------+

             ValueError occurred during pack operation:

             not enough values to unpack (expected 2, got 1)
             """
        )

        assert wrap_message(trap.value) == exp_message
        assert isinstance(trap.value.__context__, ValueError)


class TestProtections:
    def test_byteorder(self):
        exp_message = Baseline(
            """
            byteorder must be either "big" or "little"
            """
        )

        with pytest.raises(ValueError) as trap:
            # pylint: disable=unused-variable
            class Struct(Structure, byteorder="wrong"):
                pass

        assert wrap_message(trap.value) == exp_message

    def test_fmt_arg_but_no_fmt_factory(self):
        exp_message = Baseline(
            """
            when 'fmt_arg' specified, 'fmt' must be a factory function
            """
        )

        arg = member(fmt=uint8)

        with pytest.raises(TypeError) as trap:
            member(fmt=uint8, fmt_arg=arg)

        assert wrap_message(trap.value) == exp_message

    def test_default_and_compute(self):
        exp_message = Baseline(
            """
            'default' may not be specified when 'compute=True'
            """
        )

        with pytest.raises(TypeError) as trap:
            member(fmt=uint8, compute=True, default=0)

        assert wrap_message(trap.value) == exp_message

    def test_setter_when_readonly(self):
        exp_message = Baseline(
            """
            'setter' not allowed on read-only structure member properties
            """
        )

        memb = member(fmt=uint8, readonly=True)

        with pytest.raises(TypeError) as trap:

            @memb.setter
            def memb(self, value):  # pylint: disable=unused-argument
                pass

        assert wrap_message(trap.value) == exp_message

    def test_deleter(self):
        exp_message = Baseline(
            """
            structure member properties do not support 'deleter'
            """
        )

        memb = member(fmt=uint8)

        with pytest.raises(TypeError) as trap:

            @memb.deleter
            def memb(self):  # pylint: disable=unused-argument
                pass

        assert wrap_message(trap.value) == exp_message


class TestGetterOverride:

    """Test explicit member getters retained."""

    class Struct(Structure):
        memb = member(fmt=uint8)

        @memb.getter
        def memb(self):
            return 99

    def test(self):
        struct = self.Struct(memb=0)
        assert struct.memb == 99


class Pet(IntEnum):
    CAT = 0
    DOG = 1


pet_x = EnumX("pet", enum=Pet, nbytes=1)


class StructWithEnum(Structure):
    pet: Pet = member(fmt=pet_x, default=Pet.CAT)


class TestMemberEnumDefault:

    """Test member with default being an enum member."""

    expected_dump = Baseline(
        """
        +--------+--------+---------+-------+----------------+
        | Offset | Access | Value   | Bytes | Format         |
        +--------+--------+---------+-------+----------------+
        |        |        |         |       | StructWithEnum |
        | 0      | pet    | Pet.CAT | 00    | pet            |
        +--------+--------+---------+-------+----------------+
        """
    )

    def test_pack(self):
        struct = StructWithEnum()
        assert str(struct.dump) == self.expected_dump
