# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# Copyright 2021 Daniel Mark Gass, see __about__.py for license information.
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
"""Test items transform properties."""

import pytest

from plum.exceptions import SizeError
from plum.items import ItemsX
from plum.littleendian import uint8


class TestDefault:

    """Test with as many left to default as possible."""

    itemsx = ItemsX("itemsx")

    def test_name(self):
        assert self.itemsx.name == "itemsx"

    def test_nbytes(self):
        with pytest.raises(SizeError):
            return self.itemsx.nbytes

    def test_fmt(self):
        assert self.itemsx.fmt is None


class TestPositional:

    """Test explicitly defined with positional argument."""

    itemsx = ItemsX("itemsx", uint8)

    def test_name(self):
        assert self.itemsx.name == "itemsx"

    def test_nbytes(self):
        assert self.itemsx.nbytes == 1

    def test_fmt(self):
        assert self.itemsx.fmt is uint8


class TestKeyword(TestPositional):

    """Test explicitly defined with keyword argument."""

    itemsx = ItemsX(name="itemsx", fmt=uint8)
