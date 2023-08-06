# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# Copyright 2021 Daniel Mark Gass, see __about__.py for license information.
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
"""Test sized_member() member definitions."""

# pylint: disable=too-many-lines

import sys

import pytest
from baseline import Baseline

from plum.array import ArrayX
from plum.conformance import Case, CaseData, wrap_message
from plum.exceptions import UnpackError
from plum.littleendian import uint8, uint16
from plum.str import StrX
from plum.structure import Structure, member, sized_member
from plum.utilities import unpack

ascii_greedy = StrX("ascii", encoding="ascii")


class Simple(Structure):

    """Sized string."""

    size: int = member(fmt=uint8, compute=True)
    string: str = sized_member(size=size, fmt=ascii_greedy)
    bookend: int = member(fmt=uint8)


sizedstrarray = ArrayX("sizedstrarray", fmt=Simple)


class TestSimple(Case):

    data = CaseData(
        fmt=Simple,
        bindata=b"\x0cHello World!\x99",
        nbytes=None,
        values=(
            Simple(size=12, string="Hello World!", bookend=0x99),
            Simple(string="Hello World!", bookend=0x99),
        ),
        dump=Baseline(
            """
            +--------+----------+----------------+-------------------------------------+--------+
            | Offset | Access   | Value          | Bytes                               | Format |
            +--------+----------+----------------+-------------------------------------+--------+
            |        |          |                |                                     | Simple |
            |  0     | size     | 12             | 0c                                  | uint8  |
            |        | string   |                |                                     | ascii  |
            |  1     |   [0:12] | 'Hello World!' | 48 65 6c 6c 6f 20 57 6f 72 6c 64 21 |        |
            | 13     | bookend  | 153            | 99                                  | uint8  |
            +--------+----------+----------------+-------------------------------------+--------+
            """
        ),
        excess=Baseline(
            """
            +--------+----------+----------------+-------------------------------------+--------+
            | Offset | Access   | Value          | Bytes                               | Format |
            +--------+----------+----------------+-------------------------------------+--------+
            |        |          |                |                                     | Simple |
            |  0     | size     | 12             | 0c                                  | uint8  |
            |        | string   |                |                                     | ascii  |
            |  1     |   [0:12] | 'Hello World!' | 48 65 6c 6c 6f 20 57 6f 72 6c 64 21 |        |
            | 13     | bookend  | 153            | 99                                  | uint8  |
            +--------+----------+----------------+-------------------------------------+--------+
            | 14     |          | <excess bytes> | 99                                  |        |
            +--------+----------+----------------+-------------------------------------+--------+

            ExcessMemoryError occurred during unpack operation:

            1 unconsumed bytes
            """
        ),
        shortage=Baseline(
            """
        +--------+----------+----------------------+-------------------------------------+--------+
        | Offset | Access   | Value                | Bytes                               | Format |
        +--------+----------+----------------------+-------------------------------------+--------+
        |        |          |                      |                                     | Simple |
        |  0     | size     | 12                   | 0c                                  | uint8  |
        |        | string   |                      |                                     | ascii  |
        |  1     |   [0:12] | 'Hello World!'       | 48 65 6c 6c 6f 20 57 6f 72 6c 64 21 |        |
        |        | bookend  | <insufficient bytes> |                                     | uint8  |
        +--------+----------+----------------------+-------------------------------------+--------+

        InsufficientMemoryError occurred during unpack operation:

        1 too few bytes to unpack 'uint8' (1 needed, only 0 available)
        """
        ),
        implementation=Baseline(
            """
            def __init__(self, *, size: Optional[int] = None, string: str, bookend: int) -> None:
                self[:] = (size, string, bookend)

            @size.getter
            def size(self) -> int:
                if self[0] is None:
                    self[0] = self.unpack(self.ipack())[0]

                return self[0]

            @size.setter
            def size(self, value: int) -> None:
                self[0] = value

            @string.getter
            def string(self) -> str:
                return self[1]

            @string.setter
            def string(self, value: str) -> None:
                self[1] = value
                self[0] = None  # re-compute 'size' member

            @bookend.getter
            def bookend(self) -> int:
                return self[2]

            @bookend.setter
            def bookend(self, value: int) -> None:
                self[2] = value

            @classmethod
            def __pack__(cls, value, pieces: List[bytes], dump: Optional[Record] = None) -> None:
                (m_size, m_string, m_bookend) = value

                if dump is None:
                    size_pieces_index = len(pieces)
                    if m_size is None:
                        pieces.append(b"")
                    else:
                        uint8.__pack__(m_size, pieces, dump)

                    if m_size is None:
                        string_pieces_index = len(pieces)
                        cls.string.fmt.__pack__(m_string, pieces, dump)
                        m_size = len(b"".join(pieces[string_pieces_index:]))
                        uint8.__pack__(m_size, pieces, dump)
                        pieces[size_pieces_index] = pieces.pop()
                    else:
                        cls.string.fmt.__pack__(m_string, pieces, dump)

                    uint8.__pack__(m_bookend, pieces, dump)

                else:
                    size_dump = dump.add_record(access="size", fmt=uint8)
                    size_pieces_index = len(pieces)
                    if m_size is None:
                        size_dump.value = "<skipped>"
                        pieces.append(b"")
                    else:
                        uint8.__pack__(m_size, pieces, size_dump)

                    string_dump = dump.add_record(access="string", fmt=cls.string.fmt)
                    if m_size is None:
                        string_pieces_index = len(pieces)
                        cls.string.fmt.__pack__(m_string, pieces, string_dump)
                        m_size = len(b"".join(pieces[string_pieces_index:]))
                        uint8.__pack__(m_size, pieces, size_dump)
                        pieces[size_pieces_index] = pieces.pop()
                    else:
                        cls.string.fmt.__pack__(m_string, pieces, string_dump)

                    bookend_dump = dump.add_record(access="bookend", fmt=uint8)
                    uint8.__pack__(m_bookend, pieces, bookend_dump)

            @classmethod
            def __unpack__(cls, buffer: bytes, offset: int, dump: Optional[Record] = None) -> Tuple["Simple", int]:
                structure = list.__new__(cls)

                if dump is None:
                    m_size, offset = uint8.__unpack__(buffer, offset, dump)

                    buffer, string_buffer = buffer[:offset + m_size], buffer
                    if len(buffer) < offset + m_size:
                        cls.string.report_insufficient_bytes(buffer, offset, m_size)
                    m_string, offset = cls.string.fmt.__unpack__(buffer, offset, dump)
                    if offset < len(buffer):
                        cls.string.report_extra_bytes(buffer[offset:])
                    buffer = string_buffer

                    m_bookend, offset = uint8.__unpack__(buffer, offset, dump)

                else:
                    size_dump = dump.add_record(access="size", fmt=uint8)
                    m_size, offset = uint8.__unpack__(buffer, offset, size_dump)

                    string_dump = dump.add_record(access="string", fmt=cls.string.fmt)
                    buffer, string_buffer = buffer[:offset + m_size], buffer
                    if len(buffer) < offset + m_size:
                        cls.string.report_insufficient_bytes(buffer, offset, m_size, string_dump)
                    m_string, offset = cls.string.fmt.__unpack__(buffer, offset, string_dump)
                    if offset < len(buffer):
                        cls.string.report_extra_bytes(buffer[offset:], string_dump)
                    buffer = string_buffer

                    bookend_dump = dump.add_record(access="bookend", fmt=uint8)
                    m_bookend, offset = uint8.__unpack__(buffer, offset, bookend_dump)

                structure[:] = (m_size, m_string, m_bookend)

                return structure, offset

            def __eq__(self, other: Any) -> bool:
                if isinstance(other, type(self)):
                    _s_size, _s_string, _s_bookend = self
                    if _s_size is None:
                        _s_size, _s_string, _s_bookend = self.unpack(self.ipack())
                    _o_size, _o_string, _o_bookend = other
                    if _o_size is None:
                        _o_size, _o_string, _o_bookend = self.unpack(other.ipack())
                    return (_s_size, _s_string, _s_bookend) == (_o_size, _o_string, _o_bookend)
                else:
                    return list.__eq__(self, other)

            def __ne__(self, other: Any) -> bool:
                if isinstance(other, type(self)):
                    _s_size, _s_string, _s_bookend = self
                    if _s_size is None:
                        _s_size, _s_string, _s_bookend = self.unpack(self.ipack())
                    _o_size, _o_string, _o_bookend = other
                    if _o_size is None:
                        _o_size, _o_string, _o_bookend = self.unpack(other.ipack())
                    return (_s_size, _s_string, _s_bookend) != (_o_size, _o_string, _o_bookend)
                else:
                    return list.__ne__(self, other)

            def __repr__(self) -> str:
                try:
                    return f"{type(self).__name__}(size={self.size!r}, string={self.string!r}, bookend={self.bookend!r})"
                except Exception:
                    return f"{type(self).__name__}()"

            """
        ),
    )

    def test_pack_explicit_size(self):
        """Test explicit size value used instead of computed size."""
        expected_dump = Baseline(
            """
            +--------+----------+----------------+-------------------------------------+--------+
            | Offset | Access   | Value          | Bytes                               | Format |
            +--------+----------+----------------+-------------------------------------+--------+
            |        |          |                |                                     | Simple |
            |  0     | size     | 32             | 20                                  | uint8  |
            |        | string   |                |                                     | ascii  |
            |  1     |   [0:12] | 'Hello World!' | 48 65 6c 6c 6f 20 57 6f 72 6c 64 21 |        |
            | 13     | bookend  | 153            | 99                                  | uint8  |
            +--------+----------+----------------+-------------------------------------+--------+
            """
        )

        buffer, dump = Simple(
            size=32, string="Hello World!", bookend=0x99
        ).ipack_and_dump()
        assert str(dump) == expected_dump
        assert buffer == b"\x20Hello World!\x99"


class TestMetaException:
    def test_bad_reference(self):
        """Verify exception/message if sized_member gets invalid size member."""
        with pytest.raises(TypeError) as trap:

            class Bad(Structure):  # pylint: disable=unused-variable

                size: int = member(fmt=uint16, compute=True)
                array: list = sized_member(size="junk", fmt=sizedstrarray)

        expected = Baseline(
            """
            invalid 'size', must be a 'member()'
            """
        )

        assert wrap_message(trap.value) == expected

    def test_missing_association(self):
        """Verify exception/message if sized_member definition missing."""
        with pytest.raises(TypeError) as trap:

            class Bad(Structure):  # pylint: disable=unused-variable

                size: int = member(fmt=uint16, compute=True)

        expected = Baseline(
            """
            'size' member never associated with member used to compute it
            """
        )

        assert wrap_message(trap.value) == expected

    def test_excess_bytes(self):
        """Test outer limit more restrictive than inner limit (string case)."""

        class ExcessBytes(Structure):
            """Excess Bytes string."""

            size: int = member(fmt=uint8, compute=True)
            fixed: int = sized_member(size=size, fmt=uint8)

        memory_bytes = b"\x20" + bytes(32)

        with pytest.raises(UnpackError) as trap:
            unpack(ExcessBytes, memory_bytes)

        expected = Baseline(
            """
            +--------+--------+----------------+-------------------------------------------------+-------------+
            | Offset | Access | Value          | Bytes                                           | Format      |
            +--------+--------+----------------+-------------------------------------------------+-------------+
            |        |        |                |                                                 | ExcessBytes |
            |  0     | size   | 32             | 20                                              | uint8       |
            |  1     | fixed  | 0              | 00                                              | uint8       |
            +--------+--------+----------------+-------------------------------------------------+-------------+
            |  2     |        | <excess bytes> | 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 |             |
            | 18     |        |                | 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00    |             |
            +--------+--------+----------------+-------------------------------------------------+-------------+

            ExcessMemoryError occurred during unpack operation:

            31 unconsumed bytes
            """
        )

        assert wrap_message(trap.value) == expected


class Ratio(Structure):

    """Sized string with ratio usage."""

    size: int = member(fmt=uint8, compute=True)
    string: str = sized_member(size=size, fmt=ascii_greedy, ratio=2)
    bookend: int = member(fmt=uint8)


RATIO_DUMP = Baseline(
    """
    +--------+-------------+----------------+-------------------------------------+--------+
    | Offset | Access      | Value          | Bytes                               | Format |
    +--------+-------------+----------------+-------------------------------------+--------+
    |        |             |                |                                     | Ratio  |
    |  0     | size [0]    | 6              | 06                                  | uint8  |
    |        | string [1]  |                |                                     | ascii  |
    |  1     |   [0:12]    | 'Hello World!' | 48 65 6c 6c 6f 20 57 6f 72 6c 64 21 |        |
    | 13     | bookend [2] | 153            | 99                                  | uint8  |
    +--------+-------------+----------------+-------------------------------------+--------+
    """
)


class TestRatio(Case):

    """Test ratio parameter usage."""

    data = CaseData(
        fmt=Ratio,
        bindata=b"\x06Hello World!\x99",
        nbytes=None,
        values=(
            Ratio(size=6, string="Hello World!", bookend=0x99),
            Ratio(string="Hello World!", bookend=0x99),
        ),
        dump=Baseline(
            """
            +--------+----------+----------------+-------------------------------------+--------+
            | Offset | Access   | Value          | Bytes                               | Format |
            +--------+----------+----------------+-------------------------------------+--------+
            |        |          |                |                                     | Ratio  |
            |  0     | size     | 6              | 06                                  | uint8  |
            |        | string   |                |                                     | ascii  |
            |  1     |   [0:12] | 'Hello World!' | 48 65 6c 6c 6f 20 57 6f 72 6c 64 21 |        |
            | 13     | bookend  | 153            | 99                                  | uint8  |
            +--------+----------+----------------+-------------------------------------+--------+
            """
        ),
        excess=Baseline(
            """
            +--------+----------+----------------+-------------------------------------+--------+
            | Offset | Access   | Value          | Bytes                               | Format |
            +--------+----------+----------------+-------------------------------------+--------+
            |        |          |                |                                     | Ratio  |
            |  0     | size     | 6              | 06                                  | uint8  |
            |        | string   |                |                                     | ascii  |
            |  1     |   [0:12] | 'Hello World!' | 48 65 6c 6c 6f 20 57 6f 72 6c 64 21 |        |
            | 13     | bookend  | 153            | 99                                  | uint8  |
            +--------+----------+----------------+-------------------------------------+--------+
            | 14     |          | <excess bytes> | 99                                  |        |
            +--------+----------+----------------+-------------------------------------+--------+

            ExcessMemoryError occurred during unpack operation:

            1 unconsumed bytes
            """
        ),
        shortage=Baseline(
            """
        +--------+----------+----------------------+-------------------------------------+--------+
        | Offset | Access   | Value                | Bytes                               | Format |
        +--------+----------+----------------------+-------------------------------------+--------+
        |        |          |                      |                                     | Ratio  |
        |  0     | size     | 6                    | 06                                  | uint8  |
        |        | string   |                      |                                     | ascii  |
        |  1     |   [0:12] | 'Hello World!'       | 48 65 6c 6c 6f 20 57 6f 72 6c 64 21 |        |
        |        | bookend  | <insufficient bytes> |                                     | uint8  |
        +--------+----------+----------------------+-------------------------------------+--------+

        InsufficientMemoryError occurred during unpack operation:

        1 too few bytes to unpack 'uint8' (1 needed, only 0 available)
        """
        ),
        implementation=Baseline(
            """
            def __init__(self, *, size: Optional[int] = None, string: str, bookend: int) -> None:
                self[:] = (size, string, bookend)

            @size.getter
            def size(self) -> int:
                if self[0] is None:
                    self[0] = self.unpack(self.ipack())[0]

                return self[0]

            @size.setter
            def size(self, value: int) -> None:
                self[0] = value

            @string.getter
            def string(self) -> str:
                return self[1]

            @string.setter
            def string(self, value: str) -> None:
                self[1] = value
                self[0] = None  # re-compute 'size' member

            @bookend.getter
            def bookend(self) -> int:
                return self[2]

            @bookend.setter
            def bookend(self, value: int) -> None:
                self[2] = value

            @classmethod
            def __pack__(cls, value, pieces: List[bytes], dump: Optional[Record] = None) -> None:
                (m_size, m_string, m_bookend) = value

                if dump is None:
                    size_pieces_index = len(pieces)
                    if m_size is None:
                        pieces.append(b"")
                    else:
                        uint8.__pack__(m_size, pieces, dump)

                    if m_size is None:
                        string_pieces_index = len(pieces)
                        cls.string.fmt.__pack__(m_string, pieces, dump)
                        m_size = int(len(b"".join(pieces[string_pieces_index:])) // 2)
                        uint8.__pack__(m_size, pieces, dump)
                        pieces[size_pieces_index] = pieces.pop()
                    else:
                        cls.string.fmt.__pack__(m_string, pieces, dump)

                    uint8.__pack__(m_bookend, pieces, dump)

                else:
                    size_dump = dump.add_record(access="size", fmt=uint8)
                    size_pieces_index = len(pieces)
                    if m_size is None:
                        size_dump.value = "<skipped>"
                        pieces.append(b"")
                    else:
                        uint8.__pack__(m_size, pieces, size_dump)

                    string_dump = dump.add_record(access="string", fmt=cls.string.fmt)
                    if m_size is None:
                        string_pieces_index = len(pieces)
                        cls.string.fmt.__pack__(m_string, pieces, string_dump)
                        m_size = int(len(b"".join(pieces[string_pieces_index:])) // 2)
                        uint8.__pack__(m_size, pieces, size_dump)
                        pieces[size_pieces_index] = pieces.pop()
                    else:
                        cls.string.fmt.__pack__(m_string, pieces, string_dump)

                    bookend_dump = dump.add_record(access="bookend", fmt=uint8)
                    uint8.__pack__(m_bookend, pieces, bookend_dump)

            @classmethod
            def __unpack__(cls, buffer: bytes, offset: int, dump: Optional[Record] = None) -> Tuple["Ratio", int]:
                structure = list.__new__(cls)

                if dump is None:
                    m_size, offset = uint8.__unpack__(buffer, offset, dump)

                    string_nbytes = int(m_size * 2)
                    buffer, string_buffer = buffer[:offset + string_nbytes], buffer
                    if len(buffer) < offset + string_nbytes:
                        cls.string.report_insufficient_bytes(buffer, offset, string_nbytes)
                    m_string, offset = cls.string.fmt.__unpack__(buffer, offset, dump)
                    if offset < len(buffer):
                        cls.string.report_extra_bytes(buffer[offset:])
                    buffer = string_buffer

                    m_bookend, offset = uint8.__unpack__(buffer, offset, dump)

                else:
                    size_dump = dump.add_record(access="size", fmt=uint8)
                    m_size, offset = uint8.__unpack__(buffer, offset, size_dump)

                    string_dump = dump.add_record(access="string", fmt=cls.string.fmt)
                    string_nbytes = int(m_size * 2)
                    buffer, string_buffer = buffer[:offset + string_nbytes], buffer
                    if len(buffer) < offset + string_nbytes:
                        cls.string.report_insufficient_bytes(buffer, offset, string_nbytes, string_dump)
                    m_string, offset = cls.string.fmt.__unpack__(buffer, offset, string_dump)
                    if offset < len(buffer):
                        cls.string.report_extra_bytes(buffer[offset:], string_dump)
                    buffer = string_buffer

                    bookend_dump = dump.add_record(access="bookend", fmt=uint8)
                    m_bookend, offset = uint8.__unpack__(buffer, offset, bookend_dump)

                structure[:] = (m_size, m_string, m_bookend)

                return structure, offset

            def __eq__(self, other: Any) -> bool:
                if isinstance(other, type(self)):
                    _s_size, _s_string, _s_bookend = self
                    if _s_size is None:
                        _s_size, _s_string, _s_bookend = self.unpack(self.ipack())
                    _o_size, _o_string, _o_bookend = other
                    if _o_size is None:
                        _o_size, _o_string, _o_bookend = self.unpack(other.ipack())
                    return (_s_size, _s_string, _s_bookend) == (_o_size, _o_string, _o_bookend)
                else:
                    return list.__eq__(self, other)

            def __ne__(self, other: Any) -> bool:
                if isinstance(other, type(self)):
                    _s_size, _s_string, _s_bookend = self
                    if _s_size is None:
                        _s_size, _s_string, _s_bookend = self.unpack(self.ipack())
                    _o_size, _o_string, _o_bookend = other
                    if _o_size is None:
                        _o_size, _o_string, _o_bookend = self.unpack(other.ipack())
                    return (_s_size, _s_string, _s_bookend) != (_o_size, _o_string, _o_bookend)
                else:
                    return list.__ne__(self, other)

            def __repr__(self) -> str:
                try:
                    return f"{type(self).__name__}(size={self.size!r}, string={self.string!r}, bookend={self.bookend!r})"
                except Exception:
                    return f"{type(self).__name__}()"

            """
        ),
    )

    def test_pack_explicit_size(self):
        """Test explicit size value used instead of computed size."""

        expected_dump = Baseline(
            """
            +--------+----------+----------------+-------------------------------------+--------+
            | Offset | Access   | Value          | Bytes                               | Format |
            +--------+----------+----------------+-------------------------------------+--------+
            |        |          |                |                                     | Ratio  |
            |  0     | size     | 32             | 20                                  | uint8  |
            |        | string   |                |                                     | ascii  |
            |  1     |   [0:12] | 'Hello World!' | 48 65 6c 6c 6f 20 57 6f 72 6c 64 21 |        |
            | 13     | bookend  | 153            | 99                                  | uint8  |
            +--------+----------+----------------+-------------------------------------+--------+
            """
        )
        buffer, dump = Ratio(
            size=32, string="Hello World!", bookend=0x99
        ).ipack_and_dump()
        assert str(dump) == expected_dump
        assert buffer == b"\x20Hello World!\x99"


class Nested(Structure):

    """Sized array (with embedded sized strings inside)."""

    size: int = member(fmt=uint8, compute=True)
    array: list = sized_member(size=size, fmt=sizedstrarray)


NESTED_DUMP = Baseline(
    """
    +--------+--------------+----------------+-------------------------------------+---------------+
    | Offset | Access       | Value          | Bytes                               | Format        |
    +--------+--------------+----------------+-------------------------------------+---------------+
    |        |              |                |                                     | Nested        |
    |  0     | size         | 25             | 19                                  | uint8         |
    |        | array        |                |                                     | sizedstrarray |
    |        |   [0]        |                |                                     | Simple        |
    |  1     |     size     | 12             | 0c                                  | uint8         |
    |        |     string   |                |                                     | ascii         |
    |  2     |       [0:12] | 'Hello World!' | 48 65 6c 6c 6f 20 57 6f 72 6c 64 21 |               |
    | 14     |     bookend  | 153            | 99                                  | uint8         |
    |        |   [1]        |                |                                     | Simple        |
    | 15     |     size     | 9              | 09                                  | uint8         |
    |        |     string   |                |                                     | ascii         |
    | 16     |       [0:9]  | 'Good Bye!'    | 47 6f 6f 64 20 42 79 65 21          |               |
    | 25     |     bookend  | 153            | 99                                  | uint8         |
    +--------+--------------+----------------+-------------------------------------+---------------+
    """
)


class TestNested:

    memory_bytes = b"\x19\x0cHello World!\x99\x09Good Bye!\x99"
    array_value = [
        Simple(string="Hello World!", bookend=0x99),
        Simple(string="Good Bye!", bookend=0x99),
    ]

    def test_unpack(self):
        """Verify size member limits how much string member consumes."""
        nested = unpack(Nested, self.memory_bytes)
        assert str(nested.dump) == NESTED_DUMP  # pylint: disable=no-member

    def test_pack_implicit_size(self):
        """Verify size member computed from string."""
        buffer, dump = Nested(array=self.array_value).ipack_and_dump()
        assert str(dump) == NESTED_DUMP
        assert buffer == self.memory_bytes

    def test_pack_explicit_size(self):
        """Test explicit size value used instead of computed size."""
        expected_dump = Baseline(
            """
            +--------+--------------+----------------+-------------------------------------+---------------+
            | Offset | Access       | Value          | Bytes                               | Format        |
            +--------+--------------+----------------+-------------------------------------+---------------+
            |        |              |                |                                     | Nested        |
            |  0     | size         | 32             | 20                                  | uint8         |
            |        | array        |                |                                     | sizedstrarray |
            |        |   [0]        |                |                                     | Simple        |
            |  1     |     size     | 12             | 0c                                  | uint8         |
            |        |     string   |                |                                     | ascii         |
            |  2     |       [0:12] | 'Hello World!' | 48 65 6c 6c 6f 20 57 6f 72 6c 64 21 |               |
            | 14     |     bookend  | 153            | 99                                  | uint8         |
            |        |   [1]        |                |                                     | Simple        |
            | 15     |     size     | 9              | 09                                  | uint8         |
            |        |     string   |                |                                     | ascii         |
            | 16     |       [0:9]  | 'Good Bye!'    | 47 6f 6f 64 20 42 79 65 21          |               |
            | 25     |     bookend  | 153            | 99                                  | uint8         |
            +--------+--------------+----------------+-------------------------------------+---------------+
            """
        )

        assert str(Nested(size=32, array=self.array_value).dump) == expected_dump

    def test_smaller_first_limit_array(self):
        """Test outer limit more restrictive than inner limit (array case).

        Test array special as they muck with limit.

        """
        memory_bytes = b"\x06\x0cHello World!\x99"

        with pytest.raises(UnpackError) as trap:
            unpack(Nested, memory_bytes)

        expected = Baseline(
            """
            +--------+------------+----------------------+----------------+---------------+
            | Offset | Access     | Value                | Bytes          | Format        |
            +--------+------------+----------------------+----------------+---------------+
            |        |            |                      |                | Nested        |
            | 0      | size       | 6                    | 06             | uint8         |
            |        | array      |                      |                | sizedstrarray |
            |        |   [0]      |                      |                | Simple        |
            | 1      |     size   | 12                   | 0c             | uint8         |
            | 2      |     string | <insufficient bytes> | 48 65 6c 6c 6f | ascii         |
            +--------+------------+----------------------+----------------+---------------+

            InsufficientMemoryError occurred during unpack operation:

            7 too few bytes to unpack 'ascii' (12 needed, only 5 available)
            """
        )

        assert wrap_message(trap.value) == expected

    def test_smaller_first_limit_string(self):
        """Test outer limit more restrictive than inner limit (string case)."""

        class NestedStr(Structure):
            """Nested string."""

            size: int = member(fmt=uint8, compute=True)
            simple: Simple = sized_member(size=size, fmt=Simple)
            bookend: int = member(fmt=uint8)

        memory_bytes = b"\x06\x0cHello World!\x99"

        with pytest.raises(UnpackError) as trap:
            unpack(NestedStr, memory_bytes)

        expected = Baseline(
            """
            +--------+----------+----------------------+----------------+-----------+
            | Offset | Access   | Value                | Bytes          | Format    |
            +--------+----------+----------------------+----------------+-----------+
            |        |          |                      |                | NestedStr |
            | 0      | size     | 6                    | 06             | uint8     |
            |        | simple   |                      |                | Simple    |
            | 1      |   size   | 12                   | 0c             | uint8     |
            | 2      |   string | <insufficient bytes> | 48 65 6c 6c 6f | ascii     |
            +--------+----------+----------------------+----------------+-----------+

            InsufficientMemoryError occurred during unpack operation:

            7 too few bytes to unpack 'ascii' (12 needed, only 5 available)
            """
        )

        assert wrap_message(trap.value) == expected


class TestNoCompute(Case):

    """Test case where size member is not set to compute=True."""

    class Struct(Structure):
        size: int = member(fmt=uint8)
        string: str = sized_member(size=size, fmt=ascii_greedy)
        bookend: int = member(fmt=uint8)

    data = CaseData(
        fmt=Struct,
        bindata=b"\x0cHello World!\x99",
        nbytes=None,
        values=(Struct(size=12, string="Hello World!", bookend=0x99),),
        dump=Baseline(
            """
            +--------+----------+----------------+-------------------------------------+--------+
            | Offset | Access   | Value          | Bytes                               | Format |
            +--------+----------+----------------+-------------------------------------+--------+
            |        |          |                |                                     | Struct |
            |  0     | size     | 12             | 0c                                  | uint8  |
            |        | string   |                |                                     | ascii  |
            |  1     |   [0:12] | 'Hello World!' | 48 65 6c 6c 6f 20 57 6f 72 6c 64 21 |        |
            | 13     | bookend  | 153            | 99                                  | uint8  |
            +--------+----------+----------------+-------------------------------------+--------+
            """
        ),
        excess=Baseline(
            """
            +--------+----------+----------------+-------------------------------------+--------+
            | Offset | Access   | Value          | Bytes                               | Format |
            +--------+----------+----------------+-------------------------------------+--------+
            |        |          |                |                                     | Struct |
            |  0     | size     | 12             | 0c                                  | uint8  |
            |        | string   |                |                                     | ascii  |
            |  1     |   [0:12] | 'Hello World!' | 48 65 6c 6c 6f 20 57 6f 72 6c 64 21 |        |
            | 13     | bookend  | 153            | 99                                  | uint8  |
            +--------+----------+----------------+-------------------------------------+--------+
            | 14     |          | <excess bytes> | 99                                  |        |
            +--------+----------+----------------+-------------------------------------+--------+

            ExcessMemoryError occurred during unpack operation:

            1 unconsumed bytes
            """
        ),
        shortage=Baseline(
            """
        +--------+----------+----------------------+-------------------------------------+--------+
        | Offset | Access   | Value                | Bytes                               | Format |
        +--------+----------+----------------------+-------------------------------------+--------+
        |        |          |                      |                                     | Struct |
        |  0     | size     | 12                   | 0c                                  | uint8  |
        |        | string   |                      |                                     | ascii  |
        |  1     |   [0:12] | 'Hello World!'       | 48 65 6c 6c 6f 20 57 6f 72 6c 64 21 |        |
        |        | bookend  | <insufficient bytes> |                                     | uint8  |
        +--------+----------+----------------------+-------------------------------------+--------+

        InsufficientMemoryError occurred during unpack operation:

        1 too few bytes to unpack 'uint8' (1 needed, only 0 available)
        """
        ),
        implementation=Baseline(
            """
            def __init__(self, *, size: int, string: str, bookend: int) -> None:
                self[:] = (size, string, bookend)

            @size.getter
            def size(self) -> int:
                return self[0]

            @size.setter
            def size(self, value: int) -> None:
                self[0] = value

            @string.getter
            def string(self) -> str:
                return self[1]

            @string.setter
            def string(self, value: str) -> None:
                self[1] = value

            @bookend.getter
            def bookend(self) -> int:
                return self[2]

            @bookend.setter
            def bookend(self, value: int) -> None:
                self[2] = value

            @classmethod
            def __pack__(cls, value, pieces: List[bytes], dump: Optional[Record] = None) -> None:
                (m_size, m_string, m_bookend) = value

                if dump is None:
                    uint8.__pack__(m_size, pieces, dump)

                    cls.string.fmt.__pack__(m_string, pieces, dump)

                    uint8.__pack__(m_bookend, pieces, dump)

                else:
                    size_dump = dump.add_record(access="size", fmt=uint8)
                    uint8.__pack__(m_size, pieces, size_dump)

                    string_dump = dump.add_record(access="string", fmt=cls.string.fmt)
                    cls.string.fmt.__pack__(m_string, pieces, string_dump)

                    bookend_dump = dump.add_record(access="bookend", fmt=uint8)
                    uint8.__pack__(m_bookend, pieces, bookend_dump)

            @classmethod
            def __unpack__(cls, buffer: bytes, offset: int, dump: Optional[Record] = None) -> Tuple["Struct", int]:
                structure = list.__new__(cls)

                if dump is None:
                    m_size, offset = uint8.__unpack__(buffer, offset, dump)

                    buffer, string_buffer = buffer[:offset + m_size], buffer
                    if len(buffer) < offset + m_size:
                        cls.string.report_insufficient_bytes(buffer, offset, m_size)
                    m_string, offset = cls.string.fmt.__unpack__(buffer, offset, dump)
                    if offset < len(buffer):
                        cls.string.report_extra_bytes(buffer[offset:])
                    buffer = string_buffer

                    m_bookend, offset = uint8.__unpack__(buffer, offset, dump)

                else:
                    size_dump = dump.add_record(access="size", fmt=uint8)
                    m_size, offset = uint8.__unpack__(buffer, offset, size_dump)

                    string_dump = dump.add_record(access="string", fmt=cls.string.fmt)
                    buffer, string_buffer = buffer[:offset + m_size], buffer
                    if len(buffer) < offset + m_size:
                        cls.string.report_insufficient_bytes(buffer, offset, m_size, string_dump)
                    m_string, offset = cls.string.fmt.__unpack__(buffer, offset, string_dump)
                    if offset < len(buffer):
                        cls.string.report_extra_bytes(buffer[offset:], string_dump)
                    buffer = string_buffer

                    bookend_dump = dump.add_record(access="bookend", fmt=uint8)
                    m_bookend, offset = uint8.__unpack__(buffer, offset, bookend_dump)

                structure[:] = (m_size, m_string, m_bookend)

                return structure, offset

            __eq__ = list.__eq__

            __ne__ = list.__ne__

            def __repr__(self) -> str:
                try:
                    return f"{type(self).__name__}(size={self.size!r}, string={self.string!r}, bookend={self.bookend!r})"
                except Exception:
                    return f"{type(self).__name__}()"

            """
        ),
    )


class TestComputeNoSetter:

    """Test where size member is computed but sized member is r/o or explict setter."""

    def test_readonly(self):
        expected_message = Baseline(
            """
            can't set attribute 'string'
            """
        )

        class Struct(Structure):
            size: int = member(fmt=uint8, compute=True)
            string: str = sized_member(size=size, fmt=ascii_greedy, readonly=True)

        struct = Struct(string="hello world")

        with pytest.raises(AttributeError) as trap:
            struct.string = "hello"

        actual_message = str(trap.value)

        if sys.version_info < (3, 10):
            actual_message += " 'string'"

        assert actual_message == expected_message

    def test_explicit_setter(self):
        """Ensure size member not messed with explict setter."""

        class Struct(Structure):
            size: int = member(fmt=uint8, compute=True)
            string: str = sized_member(size=size, fmt=ascii_greedy)

            @string.setter
            def string(self, value):
                self[1] = value

        struct = Struct(size=5, string="hello")
        struct.string = ""

        assert struct.size == 5


class TestComputeGetter:

    """Test where size member is computed and has explict getter."""

    def test_getter(self):
        """Ensure size member getter not messed with."""

        class Struct(Structure):
            size: int = member(fmt=uint8, compute=True)

            @size.getter
            def size(self):
                return 99

            string: str = sized_member(size=size, fmt=ascii_greedy)

        struct = Struct(string="hello")

        assert struct.size == 99
