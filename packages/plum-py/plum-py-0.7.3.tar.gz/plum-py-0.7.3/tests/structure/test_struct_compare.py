# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# Copyright 2021 Daniel Mark Gass, see __about__.py for license information.
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
"""Test Structure compare."""

# pylint: disable=unneeded-not

import pytest
from baseline import Baseline

from plum.bigendian import uint8
from plum.structure import Structure, member, sized_member


class Base:

    """Test case base class."""

    Struct: Structure
    implementation_baseline: Baseline

    @staticmethod
    def iter_lines(code):
        lines = code.split("\n")

        active = False

        for line in lines:
            if "__eq__" in line or "__ne__" in line:
                active = True

            if active:
                yield line

            if not line.strip():
                active = False

    def test_generated_code(self):
        compare_implementation = "\n".join(self.iter_lines(self.Struct.implementation))
        assert compare_implementation.rstrip() == self.implementation_baseline


class TestVanilla(Base):

    """Test structure compare when no compute or ignore."""

    class Struct(Structure):

        m0: int = member(fmt=uint8)
        m1: int = member(fmt=uint8)

    implementation_baseline = Baseline(
        """
        __eq__ = list.__eq__

        __ne__ = list.__ne__
        """
    )

    struct1 = Struct(m0=0, m1=1)
    struct2 = Struct(m0=0, m1=2)

    def test_eq(self):
        assert self.struct1 == self.struct1
        assert not self.struct1 == self.struct2

    def test_ne(self):
        assert self.struct1 != self.struct2
        assert not self.struct1 != self.struct1


class TestIgnoredMember(Base):

    """Test structure compare when member set to ignore."""

    class Struct(Structure):

        m0: int = member(fmt=uint8)
        m1: int = member(fmt=uint8, ignore=True)

    implementation_baseline = Baseline(
        """
        def __eq__(self, other: Any) -> bool:
            if isinstance(other, type(self)):
                _s_m0, _s_m1 = self
                _o_m0, _o_m1 = other
                return _s_m0 == _o_m0
            else:
                return list.__eq__(self, other)

        def __ne__(self, other: Any) -> bool:
            if isinstance(other, type(self)):
                _s_m0, _s_m1 = self
                _o_m0, _o_m1 = other
                return _s_m0 != _o_m0
            else:
                return list.__ne__(self, other)
        """
    )

    struct1 = Struct(m0=0, m1=1)
    struct2 = Struct(m0=0, m1=2)
    struct3 = Struct(m0=3, m1=2)

    def test_eq(self):
        assert self.struct1 == self.struct2
        assert not self.struct1 == self.struct3

    def test_ne(self):
        assert self.struct1 != self.struct3
        assert not self.struct1 != self.struct2


class TestOneCompute(Base):

    """Test structure compare when one member computed."""

    class Struct(Structure):

        size: int = member(fmt=uint8, compute=True)
        sized: int = sized_member(fmt=uint8, size=size)

    implementation_baseline = Baseline(
        """
        def __eq__(self, other: Any) -> bool:
            if isinstance(other, type(self)):
                _s_size, _s_sized = self
                if _s_size is None:
                    _s_size, _s_sized = self.unpack(self.ipack())
                _o_size, _o_sized = other
                if _o_size is None:
                    _o_size, _o_sized = self.unpack(other.ipack())
                return (_s_size, _s_sized) == (_o_size, _o_sized)
            else:
                return list.__eq__(self, other)

        def __ne__(self, other: Any) -> bool:
            if isinstance(other, type(self)):
                _s_size, _s_sized = self
                if _s_size is None:
                    _s_size, _s_sized = self.unpack(self.ipack())
                _o_size, _o_sized = other
                if _o_size is None:
                    _o_size, _o_sized = self.unpack(other.ipack())
                return (_s_size, _s_sized) != (_o_size, _o_sized)
            else:
                return list.__ne__(self, other)
        """
    )

    struct1 = Struct(sized=2)
    struct2 = Struct(size=1, sized=2)
    struct3 = Struct(size=3, sized=2)
    struct4 = Struct(sized=4)

    def test_eq(self):
        assert self.struct1 == self.struct1
        assert self.struct1 == self.struct2
        assert not self.struct1 == self.struct3
        assert not self.struct1 == self.struct4

    def test_ne(self):
        assert self.struct1 != self.struct3
        assert self.struct1 != self.struct4
        assert not self.struct1 != self.struct1
        assert not self.struct1 != self.struct2


class TestTwoComputes(Base):

    """Test structure compare when one member computed."""

    class Struct(Structure):

        size: int = member(fmt=uint8, compute=True)
        sized: int = sized_member(fmt=uint8, size=size)

        size2: int = member(fmt=uint8, compute=True)
        sized2: int = sized_member(fmt=uint8, size=size2)

    implementation_baseline = Baseline(
        """
        def __eq__(self, other: Any) -> bool:
            if isinstance(other, type(self)):
                _s_size, _s_sized, _s_size2, _s_sized2 = self
                if None in (_s_size, _s_size2):
                    _s_size, _s_sized, _s_size2, _s_sized2 = self.unpack(self.ipack())
                _o_size, _o_sized, _o_size2, _o_sized2 = other
                if None in (_o_size, _o_size2):
                    _o_size, _o_sized, _o_size2, _o_sized2 = self.unpack(other.ipack())
                return (_s_size, _s_sized, _s_size2, _s_sized2) == (_o_size, _o_sized, _o_size2, _o_sized2)
            else:
                return list.__eq__(self, other)

        def __ne__(self, other: Any) -> bool:
            if isinstance(other, type(self)):
                _s_size, _s_sized, _s_size2, _s_sized2 = self
                if None in (_s_size, _s_size2):
                    _s_size, _s_sized, _s_size2, _s_sized2 = self.unpack(self.ipack())
                _o_size, _o_sized, _o_size2, _o_sized2 = other
                if None in (_o_size, _o_size2):
                    _o_size, _o_sized, _o_size2, _o_sized2 = self.unpack(other.ipack())
                return (_s_size, _s_sized, _s_size2, _s_sized2) != (_o_size, _o_sized, _o_size2, _o_sized2)
            else:
                return list.__ne__(self, other)
        """
    )

    struct1 = Struct(sized=2, sized2=7)
    struct2 = Struct(size=1, sized=2, sized2=7)
    struct3 = Struct(size=3, sized=2, size2=1, sized2=7)
    struct4 = Struct(sized=4, sized2=7)

    def test_eq(self):
        assert self.struct1 == self.struct1
        assert self.struct1 == self.struct2
        assert not self.struct1 == self.struct3
        assert not self.struct1 == self.struct4

    def test_ne(self):
        assert self.struct1 != self.struct3
        assert self.struct1 != self.struct4
        assert not self.struct1 != self.struct1
        assert not self.struct1 != self.struct2


class TestIgnoredCompute(Base):

    """Test structure compare when one member computed."""

    class Struct(Structure):

        size: int = member(fmt=uint8, compute=True, ignore=True)
        sized: int = sized_member(fmt=uint8, size=size)

    implementation_baseline = Baseline(
        """
        def __eq__(self, other: Any) -> bool:
            if isinstance(other, type(self)):
                _s_size, _s_sized = self
                _o_size, _o_sized = other
                return _s_sized == _o_sized
            else:
                return list.__eq__(self, other)

        def __ne__(self, other: Any) -> bool:
            if isinstance(other, type(self)):
                _s_size, _s_sized = self
                _o_size, _o_sized = other
                return _s_sized != _o_sized
            else:
                return list.__ne__(self, other)
        """
    )

    struct1 = Struct(sized=2)
    struct2 = Struct(size=1, sized=2)
    struct3 = Struct(size=3, sized=2)
    struct4 = Struct(sized=4)
    struct5 = Struct(size=1, sized=4)

    def test_eq(self):
        assert self.struct1 == self.struct1
        assert self.struct1 == self.struct2
        assert self.struct1 == self.struct3
        assert not self.struct1 == self.struct4
        assert not self.struct1 == self.struct5

    def test_ne(self):
        assert self.struct1 != self.struct4
        assert self.struct1 != self.struct5
        assert not self.struct1 != self.struct1
        assert not self.struct1 != self.struct2
        assert not self.struct1 != self.struct3


class TestIgnoreEverything(Base):

    """Test that define eq method is not overridden."""

    class Struct(Structure):

        m0: int = member(fmt=uint8, ignore=True)

    implementation_baseline = Baseline(
        """
        def __eq__(self, other: Any) -> bool:
            if isinstance(other, type(self)):
                return True
            else:
                return list.__eq__(self, other)

        def __ne__(self, other: Any) -> bool:
            if isinstance(other, type(self)):
                return False
            else:
                return list.__ne__(self, other)
        """
    )

    struct1 = Struct(m0=1)
    struct2 = Struct(m0=2)

    def test_eq(self):
        assert self.struct1 == self.struct2
        assert self.struct1 == [1]

    def test_ne(self):
        assert not self.struct1 != self.struct2
        assert not self.struct1 != [1]


class TestOverrideEq(Base):

    """Test that custom __eq__ method is not overridden."""

    class Struct(Structure):

        m0: int = member(fmt=uint8)

        def __eq__(self, other):
            raise RuntimeError("hit eq")

    implementation_baseline = Baseline(
        """
        __ne__ = list.__ne__
        """
    )

    def test_eq(self):
        with pytest.raises(RuntimeError) as trap:
            assert self.Struct(m0=1) == self.Struct(m0=1)  # pylint: disable=no-member

        assert str(trap.value) == "hit eq"


class TestOverrideNe(Base):

    """Test that custom __ne__ method is not overridden."""

    class Struct(Structure):

        m0: int = member(fmt=uint8)

        def __ne__(self, other):
            raise RuntimeError("hit ne")

    implementation_baseline = Baseline(
        """
        __eq__ = list.__eq__
        """
    )

    def test_ne(self):
        with pytest.raises(RuntimeError) as trap:
            assert self.Struct(m0=1) != self.Struct(m0=1)  # pylint: disable=no-member

        assert str(trap.value) == "hit ne"
