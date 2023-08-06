# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# Copyright 2021 Daniel Mark Gass, see __about__.py for license information.
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
"""Test IPv4AddressX transform properties."""

from plum.ipaddress import IPv4AddressX


class TestDefault:

    """Test explicitly defined with positional argument."""

    ipv4address = IPv4AddressX("ipv4address")

    def test_name(self):
        assert self.ipv4address.name == "ipv4address"

    def test_byteorder(self):
        assert self.ipv4address.byteorder == "big"

    def test_nbytes(self):
        assert self.ipv4address.nbytes == 4


class TestPositional:

    """Test explicitly defined with positional argument."""

    ipv4address = IPv4AddressX("ipv4address", "little")

    def test_name(self):
        assert self.ipv4address.name == "ipv4address"

    def test_byteorder(self):
        assert self.ipv4address.byteorder == "little"

    def test_nbytes(self):
        assert self.ipv4address.nbytes == 4


class TestKeyword(TestPositional):

    """Test explicitly defined with keyword argument."""

    ipv4address = IPv4AddressX(name="ipv4address", byteorder="little")
