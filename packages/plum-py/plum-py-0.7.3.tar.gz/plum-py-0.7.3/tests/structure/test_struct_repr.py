# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# Copyright 2021 Daniel Mark Gass, see __about__.py for license information.
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
"""Test Structure representation."""

# pylint: disable=unexpected-keyword-arg

from enum import IntEnum
from typing import Type

from baseline import Baseline

from plum.bigendian import uint8
from plum.enum import EnumX
from plum.structure import Structure, bitfield_member, member


class Register(IntEnum):

    PC = 0
    SP = 1
    R0 = 2
    R1 = 3


register = EnumX("register", Register, nbytes=1)


class Base:

    """Test case base class."""

    Sample: Type[Structure]
    sample: Structure
    implementation_baseline: Baseline
    repr_baseline: Baseline

    @staticmethod
    def iter_lines(code):
        lines = code.split("\n")

        active = False

        for line in lines:
            if "__repr__" in line:
                active = True

            if active:
                yield line

            if not line.strip():
                active = False

    def test_generated_code(self):
        compare_implementation = "\n".join(self.iter_lines(self.Sample.implementation))
        assert compare_implementation == self.implementation_baseline

    def test_repr(self):
        assert repr(self.sample) == self.repr_baseline


class TestVanilla(Base):

    """Test default structure representation (one enum, one int)."""

    class Sample(Structure):

        m0: int = bitfield_member(size=1)
        m1: int = bitfield_member(size=2, typ=Register)
        m2: int = member(fmt=uint8)
        m3: int = member(fmt=register)

    sample = Sample(m0=0, m1=Register.SP, m2=2, m3=Register.R1)

    repr_baseline = Baseline(
        """
        Sample(m0=0, m1=Register.SP, m2=2, m3=Register.R1)
        """
    )

    implementation_baseline = Baseline(
        """
        def __repr__(self) -> str:
            try:
                return f"{type(self).__name__}(m0={self.m0!r}, m1={str(self.m1)}, m2={self.m2!r}, m3={str(self.m3)})"
            except Exception:
                return f"{type(self).__name__}()"

        """
    )

    def test_repr(self):
        actual_repr = repr(self.sample)  # pylint: disable=no-member

        assert actual_repr == self.repr_baseline  # pylint: disable=no-member


class TestBlank(Base):

    """Test structure representation when one member specified as nothing."""

    class Sample(Structure):

        m0: int = member(fmt=uint8)
        m1: int = member(fmt=uint8)

    sample = Sample(m0=0, m1=1)

    repr_baseline = Baseline(
        """
        Sample(m0=0, m1=1)
        """
    )

    implementation_baseline = Baseline(
        """
        def __repr__(self) -> str:
            try:
                return f"{type(self).__name__}(m0={self.m0!r}, m1={self.m1!r})"
            except Exception:
                return f"{type(self).__name__}()"

        """
    )


class TestCustom(Base):

    """Test structure representation when one member has custom format."""

    class Sample(Structure):

        m0: int = member(fmt=uint8, argrepr="product={self.m0 * self.m1}")
        m1: int = member(fmt=uint8)

    sample = Sample(m0=3, m1=4)

    repr_baseline = Baseline(
        """
        Sample(product=12, m1=4)
        """
    )

    implementation_baseline = Baseline(
        """
        def __repr__(self) -> str:
            try:
                return f"{type(self).__name__}(product={self.m0 * self.m1}, m1={self.m1!r})"
            except Exception:
                return f"{type(self).__name__}()"

        """
    )


class TestOverride:

    """Test that custom __repr__ method is not overridden."""

    class Sample(Structure):

        m0: int = member(fmt=uint8)
        m1: int = member(fmt=uint8)

        def __repr__(self):
            return "CustomRepresentation"

    def test_repr(self):
        assert repr(self.Sample(m0=0, m1=1)) == "CustomRepresentation"
