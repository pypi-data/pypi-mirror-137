# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# Copyright 2021 Daniel Mark Gass, see __about__.py for license information.
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
"""Test Structure type inheritance behaviors."""

from baseline import Baseline

from plum.littleendian import uint8
from plum.structure import Structure, member


class Base(Structure):

    m0 = member(fmt=uint8)
    m1 = member(fmt=uint8)


class TestAddMethod:

    """Inherit members, but just add a method."""

    class Struct(Base):
        @property
        def product(self):
            return self.m0 * self.m1

    def test_init_and_property(self):
        assert self.Struct(m0=2, m1=3).product == 6

    def test_round_trip(self):
        expected_dump = Baseline(
            """
            +--------+--------+-------+-------+--------+
            | Offset | Access | Value | Bytes | Format |
            +--------+--------+-------+-------+--------+
            |        |        |       |       | Struct |
            | 0      | m0     | 1     | 01    | uint8  |
            | 1      | m1     | 2     | 02    | uint8  |
            +--------+--------+-------+-------+--------+
            """
        )
        original = self.Struct(m0=1, m1=2)
        buffer, pack_dump = original.ipack_and_dump()
        copy, unpack_dump = self.Struct.unpack_and_dump(buffer)
        assert str(pack_dump) == expected_dump
        assert str(unpack_dump) == expected_dump
        assert original == copy


class TestAddMembers:

    """Inherit members, but just add a method."""

    class Struct(Base):

        m2 = member(fmt=uint8)
        m3 = member(fmt=uint8)

    def test_round_trip(self):
        expected_dump = Baseline(
            """
            +--------+--------+-------+-------+--------+
            | Offset | Access | Value | Bytes | Format |
            +--------+--------+-------+-------+--------+
            |        |        |       |       | Struct |
            | 0      | m0     | 1     | 01    | uint8  |
            | 1      | m1     | 2     | 02    | uint8  |
            | 2      | m2     | 3     | 03    | uint8  |
            | 3      | m3     | 4     | 04    | uint8  |
            +--------+--------+-------+-------+--------+
            """
        )
        original = self.Struct(m0=1, m1=2, m2=3, m3=4)
        buffer, pack_dump = original.ipack_and_dump()
        copy, unpack_dump = self.Struct.unpack_and_dump(buffer)
        assert str(pack_dump) == expected_dump
        assert str(unpack_dump) == expected_dump
        assert original == copy
