# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# Copyright 2021 Daniel Mark Gass, see __about__.py for license information.
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
"""Test miscellaneous StrX transform features."""

import pytest

from baseline import Baseline

from plum.conformance import wrap_message
from plum.exceptions import PackError, UnpackError
from plum.str import StrX
from plum.utilities import pack, pack_and_dump, unpack, unpack_and_dump

ascii_greedy = StrX("ascii_greedy", encoding="ascii")
ascii_zero = StrX("ascii_zero", encoding="ascii", zero_termination=True)
custom = StrX("custom", encoding="ascii")
utf8 = StrX("utf8", encoding="utf8")
ascii_ignore = StrX("ascii_ignore", encoding="ascii", errors="ignore")


class TestUnpack:

    """Test various unpack() corner cases."""

    def test_zero_term_decoding_error(self):
        """Test unpacking a zero terminated string that has an invalid encoding."""

        with pytest.raises(UnpackError) as trap:
            unpack(ascii_zero, b"hello\x80world\x00")

        expected = Baseline(
            """
            +--------+-----------+---------+----------------------+------------+
            | Offset | Access    | Value   | Bytes                | Format     |
            +--------+-----------+---------+----------------------+------------+
            |        |           |         |                      | ascii_zero |
            |  0     | [0:5]     | 'hello' | 68 65 6c 6c 6f       |            |
            |  5     | --error-- |         | 80 77 6f 72 6c 64 00 |            |
            +--------+-----------+---------+----------------------+------------+

            UnicodeDecodeError occurred during unpack operation:

            'ascii' codec can't decode byte 0x80 in position 0: ordinal not in
            range(128)
            """
        )

        assert wrap_message(trap.value) == expected

    def test_multibyte_chars(self):
        """Test unpacking characters that are more than one byte."""
        sample, dump = unpack_and_dump(
            utf8, b"Mohu j\xc3\xadst sklo, neubl\xc3\xad\xc5\xbe\xc3\xad mi."
        )
        assert sample == "Mohu jíst sklo, neublíží mi."

        # pylint: disable=line-too-long
        expected = Baseline(
            """
            +--------+---------+-------------------+-------------------------------------------------+--------+
            | Offset | Access  | Value             | Bytes                                           | Format |
            +--------+---------+-------------------+-------------------------------------------------+--------+
            |        |         |                   |                                                 | utf8   |
            |  0     | [0:15]  | 'Mohu j\xedst sklo,' | 4d 6f 68 75 20 6a c3 ad 73 74 20 73 6b 6c 6f 2c |        |
            | 16     | [15:28] | ' neubl\xed\u017e\xed mi.'   | 20 6e 65 75 62 6c c3 ad c5 be c3 ad 20 6d 69 2e |        |
            +--------+---------+-------------------+-------------------------------------------------+--------+
            """
        )

        assert str(dump) == expected

    def test_multibyte_chars_byte_shortage(self):
        """Test unpacking characters that are more than one byte but short bytes."""
        with pytest.raises(UnpackError) as trap:
            unpack_and_dump(utf8, b"Mohu j\xc3")

        # pylint: disable=line-too-long
        expected = Baseline(
            """
            +--------+--------+----------+----------------------+--------+
            | Offset | Access | Value    | Bytes                | Format |
            +--------+--------+----------+----------------------+--------+
            |        |        |          |                      | utf8   |
            | 0      | [0:6]  | 'Mohu j' | 4d 6f 68 75 20 6a c3 |        |
            +--------+--------+----------+----------------------+--------+

            UnicodeDecodeError occurred during unpack operation:

            'utf-8' codec can't decode byte 0xc3 in position 0: unexpected end of
            data
            """
        )

        assert wrap_message(trap.value) == expected


class TestPack:

    """Test various pack() corner cases."""

    def test_encoding_error(self):
        """Test packing a string that can't be encoded."""
        expected = Baseline(
            r"""
            +--------+-----------+-----------------------+----------------------------+--------------+
            | Offset | Access    | Value                 | Bytes                      | Format       |
            +--------+-----------+-----------------------+----------------------------+--------------+
            |        |           |                       |                            | ascii_greedy |
            | 0      | [0:9]     | 'The quick'           | 54 68 65 20 71 75 69 63 6b |              |
            |        | --error-- | '\x80brown fox jumps' |                            |              |
            |        |           | ' over the lazy d'    |                            |              |
            |        |           | 'og'                  |                            |              |
            +--------+-----------+-----------------------+----------------------------+--------------+

            UnicodeEncodeError occurred during pack operation:

            'ascii' codec can't encode character '\x80' in position 0: ordinal not
            in range(128)
            """
        )

        with pytest.raises(PackError) as trap:
            # include more than 16 characters after the problem to
            # exercise the dump logic to break up the string
            pack("The quick\x80brown fox jumps over the lazy dog", ascii_greedy)

        assert wrap_message(trap.value) == expected

    def test_exceeds_size(self):
        """Test packing a string that exceeds the size limit."""

        sized_ascii = StrX("sized_ascii", nbytes=5, encoding="ascii")

        expected = Baseline(
            """
            +--------+--------+----------+-------------------+-------------+
            | Offset | Access | Value    | Bytes             | Format      |
            +--------+--------+----------+-------------------+-------------+
            |        |        |          |                   | sized_ascii |
            | 0      | [0:6]  | 'hello!' | 68 65 6c 6c 6f 21 |             |
            +--------+--------+----------+-------------------+-------------+

            TypeError occurred during pack operation:

            sized_ascii number of string bytes (6) exceeds limit (5)
            """
        )

        with pytest.raises(PackError) as trap:
            pack("hello!", sized_ascii)

        assert wrap_message(trap.value) == expected


class TestPackAndDump:

    """Test various pack_and_dump() corner cases."""

    def test_empty(self):
        """Test empty string pack."""
        expected_dump = Baseline(
            """
            +--------+--------+-------+-------+--------+
            | Offset | Access | Value | Bytes | Format |
            +--------+--------+-------+-------+--------+
            |        |        |       |       | custom |
            |        | [0:0]  | ''    |       |        |
            +--------+--------+-------+-------+--------+
            """
        )

        buffer, dump = pack_and_dump("", custom)

        assert buffer == b""
        assert str(dump) == expected_dump

    def test_one_full_dump_row(self):
        """Test string exactly size of one dump row."""
        expected_dump = Baseline(
            """
            +--------+--------+--------------------+-------------------------------------------------+--------+
            | Offset | Access | Value              | Bytes                                           | Format |
            +--------+--------+--------------------+-------------------------------------------------+--------+
            |        |        |                    |                                                 | custom |
            |  0     | [0:16] | '0123456789abcdef' | 30 31 32 33 34 35 36 37 38 39 61 62 63 64 65 66 |        |
            +--------+--------+--------------------+-------------------------------------------------+--------+
            """
        )

        sample = "0123456789abcdef"
        buffer, dump = pack_and_dump(sample, custom)

        assert buffer == bytearray(sample, encoding="ascii")
        assert str(dump) == expected_dump

    def test_two_full_dump_row(self):
        """Test string exactly size of one dump row."""
        expected_dump = Baseline(
            """
            +--------+---------+--------------------+-------------------------------------------------+--------+
            | Offset | Access  | Value              | Bytes                                           | Format |
            +--------+---------+--------------------+-------------------------------------------------+--------+
            |        |         |                    |                                                 | custom |
            |  0     | [0:16]  | '0123456789abcdef' | 30 31 32 33 34 35 36 37 38 39 61 62 63 64 65 66 |        |
            | 16     | [16:32] | '0123456789abcdef' | 30 31 32 33 34 35 36 37 38 39 61 62 63 64 65 66 |        |
            +--------+---------+--------------------+-------------------------------------------------+--------+
            """
        )

        sample = "0123456789abcdef" * 2
        buffer, dump = pack_and_dump(sample, custom)

        assert buffer == bytearray(sample, encoding="ascii")
        assert str(dump) == expected_dump


class TestErrors:

    """Test "errors" property."""

    def test_replace(self):
        assert ascii_ignore.unpack(b"hello\x80world") == "helloworld"


class TestFixedSizeZeroTerm:

    ascii_zero = StrX(
        "ascii_zero", encoding="ascii", zero_termination=True, nbytes=10, pad=b"\x00"
    )

    def test_unpack(self):
        assert self.ascii_zero.unpack(b"hello\x00fill") == "hello"

    def test_unpack_and_dump(self):
        expected_dump = Baseline(
            """
            +--------+-----------------+---------+----------------+------------+
            | Offset | Access          | Value   | Bytes          | Format     |
            +--------+-----------------+---------+----------------+------------+
            |        |                 |         |                | ascii_zero |
            |  0     | [0:5]           | 'hello' | 68 65 6c 6c 6f |            |
            |  5     | --termination-- |         | 00             |            |
            |  6     | --pad--         |         | 66 69 6c 6c    |            |
            +--------+-----------------+---------+----------------+------------+
            """
        )

        string, dump = self.ascii_zero.unpack_and_dump(b"hello\x00fill")

        assert str(dump) == expected_dump
        assert string == "hello"

    def test_pack(self):
        assert self.ascii_zero.pack("hello") == b"hello" + bytes(5)

    def test_pack_and_dump(self):
        expected_dump = Baseline(
            """
            +--------+-----------------+---------+----------------+------------+
            | Offset | Access          | Value   | Bytes          | Format     |
            +--------+-----------------+---------+----------------+------------+
            |        |                 |         |                | ascii_zero |
            |  0     | [0:5]           | 'hello' | 68 65 6c 6c 6f |            |
            |  5     | --termination-- |         | 00             |            |
            |  6     | --pad--         |         | 00 00 00 00    |            |
            +--------+-----------------+---------+----------------+------------+
            """
        )

        buffer, dump = self.ascii_zero.pack_and_dump("hello")

        assert str(dump) == expected_dump
        assert buffer == b"hello" + bytes(5)


class TestFixedSizeZeroTermNoPad:

    ascii_zero = StrX("ascii_zero", encoding="ascii", zero_termination=True, nbytes=10)

    unpack_message = Baseline(
        """


        +--------+----------------------+-------------------+------------+
        | Offset | Value                | Bytes             | Format     |
        +--------+----------------------+-------------------+------------+
        | 0      | <insufficient bytes> | 68 65 6c 6c 6f 00 | ascii_zero |
        +--------+----------------------+-------------------+------------+

        InsufficientMemoryError occurred during unpack operation:

        4 too few bytes to unpack 'ascii_zero' (10 needed, only 6 available)
        """
    )

    def test_unpack(self):
        with pytest.raises(UnpackError) as trap:
            self.ascii_zero.unpack(b"hello\x00")

        assert str(trap.value) == self.unpack_message

    def test_unpack_and_dump(self):
        with pytest.raises(UnpackError) as trap:
            self.ascii_zero.unpack_and_dump(b"hello\x00")

        assert str(trap.value) == self.unpack_message

    pack_message = Baseline(
        """


        +--------+-----------------+---------+----------------+------------+
        | Offset | Access          | Value   | Bytes          | Format     |
        +--------+-----------------+---------+----------------+------------+
        |        |                 |         |                | ascii_zero |
        | 0      | [0:5]           | 'hello' | 68 65 6c 6c 6f |            |
        | 5      | --termination-- |         | 00             |            |
        +--------+-----------------+---------+----------------+------------+

        ValueError occurred during pack operation:

        ascii_zero number of string bytes (6) falls short of (10)
        """
    )

    def test_pack(self):
        with pytest.raises(PackError) as trap:
            self.ascii_zero.pack("hello")

        assert str(trap.value) == self.pack_message

    def pack_and_dump(self):
        with pytest.raises(PackError) as trap:
            self.ascii_zero.pack_and_dump("hello")

        assert str(trap.value) == self.pack_message


class TestPadNotNeeded:

    ascii_fixed = StrX("ascii_fixed", encoding="ascii", nbytes=5, pad=b"\x00")

    def test_pack(self):
        assert self.ascii_fixed.pack("hello") == b"hello"

    def test_pack_and_dump(self):
        expected_dump = Baseline(
            """
            +--------+--------+---------+----------------+-------------+
            | Offset | Access | Value   | Bytes          | Format      |
            +--------+--------+---------+----------------+-------------+
            |        |        |         |                | ascii_fixed |
            | 0      | [0:5]  | 'hello' | 68 65 6c 6c 6f |             |
            +--------+--------+---------+----------------+-------------+
            """
        )

        buffer, dump = self.ascii_fixed.pack_and_dump("hello")

        assert str(dump) == expected_dump
        assert buffer == b"hello"
