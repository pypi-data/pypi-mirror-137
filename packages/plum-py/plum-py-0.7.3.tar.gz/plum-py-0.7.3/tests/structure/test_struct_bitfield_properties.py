# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# Copyright 2021 Daniel Mark Gass, see __about__.py for license information.
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
"""Test BitFieldMember properties."""

from baseline import Baseline

from plum.structure import Structure, bitfield_member


class Struct(Structure):
    defaulted_bitfield = bitfield_member("doc", size=3)
    kw_bitfield = bitfield_member(
        doc="kw doc",
        size=4,
        lsb=4,
        typ=bool,
        signed=True,
        default=1,
        ignore=True,
        readonly=True,
        compute=False,
        nbytes=2,
        argrepr="argrepr",
    )


class TestDefault:

    """Test with as many left to default as possible."""

    def test_argrepr(self):
        expected = Baseline(
            """
            defaulted_bitfield={self.defaulted_bitfield!r}
            """
        )
        assert Struct.defaulted_bitfield.argrepr == expected

    def test_compute(self):
        assert Struct.defaulted_bitfield.compute is False

    def test_default(self):
        assert Struct.defaulted_bitfield.default is None

    def test_doc(self):
        assert Struct.defaulted_bitfield.doc == "doc"

    def test_ignore(self):
        assert Struct.defaulted_bitfield.ignore is False

    def test_lsb(self):
        assert Struct.defaulted_bitfield.lsb == 0

    def test_name(self):
        assert Struct.defaulted_bitfield.name == "defaulted_bitfield"

    def test_nbytes(self):
        assert Struct.defaulted_bitfield.nbytes == 1

    def test_readonly(self):
        assert Struct.defaulted_bitfield.readonly is False

    def test_signed(self):
        assert Struct.defaulted_bitfield.signed is False

    def test_size(self):
        assert Struct.defaulted_bitfield.size == 3

    def test_typ(self):
        assert Struct.defaulted_bitfield.typ is int


class TestKeyword:

    """Test explicitly defined with keyword argument."""

    def test_argrepr(self):
        assert Struct.kw_bitfield.argrepr == "argrepr"

    def test_compute(self):
        assert Struct.kw_bitfield.compute is False

    def test_default(self):
        assert Struct.kw_bitfield.default == 1

    def test_doc(self):
        assert Struct.kw_bitfield.doc == "kw doc"

    def test_ignore(self):
        assert Struct.kw_bitfield.ignore is True

    def test_lsb(self):
        assert Struct.kw_bitfield.lsb == 4

    def test_name(self):
        assert Struct.kw_bitfield.name == "kw_bitfield"

    def test_nbytes(self):
        assert Struct.kw_bitfield.nbytes == 2

    def test_readonly(self):
        assert Struct.kw_bitfield.readonly is True

    def test_signed(self):
        assert Struct.kw_bitfield.signed is True

    def test_size(self):
        assert Struct.kw_bitfield.size == 4

    def test_typ(self):
        assert Struct.kw_bitfield.typ is bool
