# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# Copyright 2021 Daniel Mark Gass, see __about__.py for license information.
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
"""Test BitFields data store transform properties."""
# pylint: disable=comparison-with-callable

from plum.bitfields import BitFields, bitfield


class TestDefault:

    """Test with as many left to default as possible."""

    class Sample(BitFields):

        """Sample bit fields data store transform type."""

        m0: int = bitfield(size=1)
        m1: int = bitfield(size=1)

    def test_nbytes(self):
        assert self.Sample.nbytes == 1
        assert self.Sample.from_int(0).nbytes == 1

    def test_byteorder(self):
        assert self.Sample.byteorder == "little"

    def test_default(self):
        assert self.Sample.default == 0

    def test_ignore(self):
        assert self.Sample.ignore == 0

    def test_nested(self):
        assert self.Sample.nested is False


class TestKeyword:

    """Test explicitly defined with keyword argument."""

    class Sample(
        BitFields, nbytes=2, byteorder="big", default=1, ignore=2, nested=True
    ):

        """Sample bit fields data store transform type."""

        m0: int = bitfield(size=1)
        m1: int = bitfield(size=1)

    def test_nbytes(self):
        assert self.Sample.nbytes == 2
        assert self.Sample.from_int(0).nbytes == 2

    def test_byteorder(self):
        assert self.Sample.byteorder == "big"

    def test_default(self):
        assert self.Sample.default == 1

    def test_ignore(self):
        assert self.Sample.ignore == 2

    def test_nested(self):
        assert self.Sample.nested is True
