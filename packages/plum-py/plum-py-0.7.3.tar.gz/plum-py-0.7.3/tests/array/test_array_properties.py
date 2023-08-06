# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# Copyright 2021 Daniel Mark Gass, see __about__.py for license information.
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
"""Test float transform properties."""

import pytest

from plum.array import ArrayX
from plum.exceptions import SizeError
from plum.littleendian import uint8
from plum.str import StrX

ascii_zero = StrX("ascii_zero", encoding="ascii", zero_termination=True)


class TestDefault:

    """Test with as many left to default as possible."""

    arrayx = ArrayX("arrayx", uint8)

    def test_name(self):
        assert self.arrayx.name == "arrayx"

    def test_nbytes(self):
        with pytest.raises(SizeError):
            return self.arrayx.nbytes

    def test_fmt(self):
        assert self.arrayx.fmt is uint8

    def test_dims(self):
        return self.arrayx.dims == (None,)


class TestPositional:

    """Test explicitly defined with positional argument."""

    arrayx = ArrayX("arrayx", uint8, (2,))

    def test_name(self):
        assert self.arrayx.name == "arrayx"

    def test_nbytes(self):
        assert self.arrayx.nbytes == 2

    def test_fmt(self):
        assert self.arrayx.fmt is uint8

    def test_dims(self):
        return self.arrayx.dims == (2,)


class TestKeyword(TestPositional):

    """Test explicitly defined with keyword argument."""

    arrayx = ArrayX(name="arrayx", fmt=uint8, dims=(2,))


class TestVariable:

    """Test nbytes property when member size is variable."""

    arrayx = ArrayX(name="arrayx", fmt=ascii_zero, dims=(2,))

    def test_nbytes(self):
        with pytest.raises(SizeError):
            return self.arrayx.nbytes
