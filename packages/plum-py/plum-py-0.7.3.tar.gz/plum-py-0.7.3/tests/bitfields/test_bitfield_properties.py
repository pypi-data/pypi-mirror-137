# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# Copyright 2021 Daniel Mark Gass, see __about__.py for license information.
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
"""Test BitField properties."""

import pytest

from baseline import Baseline

from plum.bitfields import BitFields, bitfield
from plum.conformance import wrap_message
from plum.enum import EnumX

from sample_bitfields import Register

register = EnumX("register", Register)


class Fields(BitFields, fieldorder="least_to_most"):

    defaulted_bitfield = bitfield("doc", size=3)

    kw_bitfield = bitfield(
        doc="kw doc",
        size=4,
        typ=bool,
        lsb=8,
        default=1,
        signed=True,
        ignore=True,
        readonly=True,
        argrepr="argrepr",
    )


class TestDefault:

    """Test with as many left to default as possible."""

    def test_argrepr(self):
        assert (
            Fields.defaulted_bitfield.argrepr
            == "defaulted_bitfield={self.defaulted_bitfield!r}"
        )

    def test_default(self):
        assert Fields.defaulted_bitfield.default is None

    def test_doc(self):
        assert Fields.defaulted_bitfield.doc == "doc"

    def test_ignore(self):
        assert Fields.defaulted_bitfield.ignore is False

    def test_lsb(self):
        assert Fields.defaulted_bitfield.lsb == 0

    def test_mask(self):
        assert Fields.defaulted_bitfield.mask == 7

    def test_minvalue(self):
        assert Fields.defaulted_bitfield.minvalue == 0

    def test_maxvalue(self):
        assert Fields.defaulted_bitfield.maxvalue == 7

    def test_name(self):
        assert Fields.defaulted_bitfield.name == "defaulted_bitfield"

    def test_readonly(self):
        assert Fields.defaulted_bitfield.readonly is False

    def test_signbit(self):
        assert Fields.defaulted_bitfield.signbit == 0

    def test_signed(self):
        assert Fields.defaulted_bitfield.signed is False

    def test_size(self):
        assert Fields.defaulted_bitfield.size == 3

    def test_type_hint(self):
        assert Fields.defaulted_bitfield.type_hint is int

    def test_typ(self):
        assert Fields.defaulted_bitfield.typ is int


class TestKeyword:

    """Test explicitly defined with keyword argument."""

    def test_argrepr(self):
        assert Fields.kw_bitfield.argrepr == "argrepr"

    def test_default(self):
        assert Fields.kw_bitfield.default == 1

    def test_doc(self):
        assert Fields.kw_bitfield.doc == "kw doc"

    def test_ignore(self):
        assert Fields.kw_bitfield.ignore is True

    def test_lsb(self):
        assert Fields.kw_bitfield.lsb == 8

    def test_mask(self):
        assert Fields.kw_bitfield.mask == 0xF

    def test_minvalue(self):
        assert Fields.kw_bitfield.minvalue == -8

    def test_maxvalue(self):
        assert Fields.kw_bitfield.maxvalue == 7

    def test_name(self):
        assert Fields.kw_bitfield.name == "kw_bitfield"

    def test_readonly(self):
        assert Fields.kw_bitfield.readonly is True

    def test_signbit(self):
        assert Fields.kw_bitfield.signbit == 0x8

    def test_signed(self):
        assert Fields.kw_bitfield.signed is True

    def test_size(self):
        assert Fields.kw_bitfield.size == 4

    def test_type_hint(self):
        assert Fields.kw_bitfield.type_hint is bool

    def test_typ(self):
        assert Fields.kw_bitfield.typ is bool


class TestEnum:

    """Test special handling for EnumX type hints."""

    def test_enumx_hint(self):
        bitfield_ = bitfield(size=2, typ=register)
        assert bitfield_.type_hint is Register


class TestReadOnly:
    def test_decorator(self):
        expected_message = Baseline(
            """
            'setter' not allowed on read-only bit field properties
            """
        )

        bitfield_ = bitfield(size=2, readonly=True)

        with pytest.raises(TypeError) as trap:

            @bitfield_.setter
            def bitfield_(self, value):
                # pylint: disable=unused-argument
                pass

        assert wrap_message(trap.value) == expected_message


class TestDeleter:
    def test_deleter_blocked(self):
        expected_message = Baseline(
            """
            bit field properties do not support 'deleter'
            """
        )

        bitfield_ = bitfield(size=2, readonly=True)

        with pytest.raises(TypeError) as trap:

            @bitfield_.deleter
            def bitfield_(self):
                # pylint: disable=unused-argument
                pass

        assert wrap_message(trap.value) == expected_message
