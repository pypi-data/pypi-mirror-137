# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# Copyright 2021 Daniel Mark Gass, see __about__.py for license information.
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
"""Test structure subclasses can override methods."""

from plum.littleendian import uint8
from plum.structure import Structure, member


class Sample(Structure):

    """Sample structure type with method overrides."""

    mbr1: int = member(fmt=uint8, ignore=True)

    def __init__(self, mbr1=0x88):
        """CUSTOM INIT"""
        # pylint: disable=super-init-not-called
        list.append(self, mbr1)

    @classmethod
    def __pack__(cls, value, pieces, dump=None):
        pieces.append(b"\x99")

    @classmethod
    def __unpack__(cls, buffer, offset, dump=None):
        structure = list.__new__(cls)
        structure[0:0] = (0x88,)
        return structure, offset + 1

    def asdict(self):
        """Return structure members in dictionary form.

        :returns: structure members
        :rtype: dict

        """
        return {"hello": "world"}

    def __eq__(self, other):
        return "__eq__"

    def __ne__(self, other):
        return "__ne__"

    def __getattr__(self, name):
        return "__getattr__"

    def __setattr__(self, name, value):
        object.__setattr__(self, name, value)


class TestOverrides:

    """Test structure subclasses can override methods.

    Certain methods are created automatically by the structure metaclass.
    Verify they all can be overridden with a custom method.

    """

    @staticmethod
    def test_init():
        """Test __init__() may be overridden."""
        assert Sample() == [0x88]

    @staticmethod
    def test_asdict():
        """Test asdict() may be overridden."""
        assert Sample().asdict() == {"hello": "world"}

    @staticmethod
    def test_pack():
        """Test __pack__() may be overridden."""
        assert Sample().ipack() == b"\x99"

    @staticmethod
    def test_unpack():
        """Test __unpack__() may be overridden."""
        sample = Sample.unpack(b"\x99")
        assert sample.mbr1 == 0x88

    @staticmethod
    def test_eq():
        """Test __eq__() may be overridden."""
        assert Sample().__eq__(None) == "__eq__"

    @staticmethod
    def test_ne():
        """Test __ne__() may be overridden."""
        assert Sample().__ne__(None) == "__ne__"

    @staticmethod
    def test_getattr():
        """Test __getattr__() may be overridden."""
        assert Sample().junk == "__getattr__"

    @staticmethod
    def test_setattr():
        """Test __getattr__() may be overridden."""
        sample = Sample()
        sample.junk = "junk"  # pylint: disable=attribute-defined-outside-init
        assert object.__getattribute__(sample, "junk") == "junk"
