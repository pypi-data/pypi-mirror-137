# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# Copyright 2021 Daniel Mark Gass, see __about__.py for license information.
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
"""Test Structure representation."""

# pylint: disable=unexpected-keyword-arg

from typing import Type

from baseline import Baseline

from plum.bitfields import BitFields, bitfield

from sample_bitfields import Register


class Base:

    """Test case base class."""

    Sample: Type[BitFields]
    sample: BitFields
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

    class Sample(BitFields):

        """Sample bit fields data store transform type."""

        m0: int = bitfield(size=1)
        m1: int = bitfield(size=1, typ=Register)

    sample = Sample(m0=0, m1=Register.SP)

    repr_baseline = Baseline(
        """
        Sample(m0=0, m1=Register.SP)
        """
    )

    implementation_baseline = Baseline(
        """
        def __repr__(self) -> str:
            try:
                return f"{type(self).__name__}(m0={self.m0!r}, m1={str(self.m1)})"
            except Exception:
                return f"{type(self).__name__}()"

        """
    )

    def test_repr(self):
        actual_repr = repr(self.sample)  # pylint: disable=no-member

        assert actual_repr == self.repr_baseline  # pylint: disable=no-member


class TestBlank(Base):

    """Test structure representation when one member specified as nothing."""

    class Sample(BitFields):

        """Sample bit fields data store transform type."""

        m0: int = bitfield(size=1, argrepr="")
        m1: int = bitfield(size=1)

    sample = Sample(m0=0, m1=1)

    repr_baseline = Baseline(
        """
        Sample(m1=1)
        """
    )

    implementation_baseline = Baseline(
        """
        def __repr__(self) -> str:
            try:
                return f"{type(self).__name__}(m1={self.m1!r})"
            except Exception:
                return f"{type(self).__name__}()"

        """
    )


class TestCustom(Base):

    """Test structure representation when one member has custom format."""

    class Sample(BitFields):

        """Sample bit fields data store transform type."""

        m0: int = bitfield(size=1, argrepr="product={self.m0 * self.m1}")
        m1: int = bitfield(size=1)

    sample = Sample(m0=0, m1=1)

    repr_baseline = Baseline(
        """
        Sample(product=0, m1=1)
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

    class Sample(BitFields):

        """Sample bit fields data store transform type."""

        m0: int = bitfield(size=1, argrepr="product={_m0 * _m1}")
        m1: int = bitfield(size=1)

        def __repr__(self):
            return "CustomRepresentation"

    def test_repr(self):
        assert repr(self.Sample(m0=0, m1=1)) == "CustomRepresentation"
