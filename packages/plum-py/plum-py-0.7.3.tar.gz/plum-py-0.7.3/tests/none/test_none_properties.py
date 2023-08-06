# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# Copyright 2021 Daniel Mark Gass, see __about__.py for license information.
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
"""Test NoneX transform properties."""

from plum.none import NoneX


class TestPositional:

    """Test explicitly defined with positional argument."""

    nonex = NoneX("nonex")

    def test_name(self):
        assert self.nonex.name == "nonex"

    def test_nbytes(self):
        assert self.nonex.nbytes == 0


class TestKeyword(TestPositional):

    """Test explicitly defined with keyword argument."""

    nonex = NoneX(name="nonex")
