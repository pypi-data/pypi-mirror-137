# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# Copyright 2021 Daniel Mark Gass, see __about__.py for license information.
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
"""Test structure data store transform properties."""

# pylint doesn't seem happy with properties in metaclass
# pylint: disable=comparison-with-callable

import pytest

from plum.array import ArrayX
from plum.bigendian import uint8
from plum.exceptions import SizeError
from plum.structure import Structure, member


class TestDefault:
    """Test with as many left to default as possible."""

    class Struct(Structure):
        m0 = member(fmt=uint8)

    def test_byteorder(self):
        assert self.Struct.byteorder == "little"

    def test_nbytes(self):
        assert self.Struct.nbytes == 1
        assert self.Struct(m0=0).nbytes == 1


class TestKeyword:

    """Test explicitly defined with keyword argument."""

    class Struct(Structure, byteorder="big"):
        m0 = member(fmt=ArrayX("array", fmt=uint8))

    def test_byteorder(self):
        assert self.Struct.byteorder == "big"

    def test_nbytes(self):
        with pytest.raises(SizeError):
            self.Struct.nbytes  # pylint: disable=pointless-statement
        assert self.Struct(m0=[0]).nbytes == 1
