# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# Copyright 2021 Daniel Mark Gass, see __about__.py for license information.
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
"""Test format factory function as format."""

import pytest
from baseline import Baseline

from plum.conformance import Case, CaseData, wrap_message
from plum.littleendian import uint8, uint16
from plum.structure import Structure, member


class TestFmtArg(Case):

    """Factory passed member as controlled by 'fmt_arg'."""

    class Struct(Structure):

        datatype: int = member(fmt=uint8)
        data: int = member(fmt_arg=datatype, fmt={0: uint8, 1: uint16}.__getitem__)
        bookend: int = member(fmt=uint8)

    data = CaseData(
        fmt=Struct,
        bindata=bytes.fromhex("000177"),
        nbytes=None,
        values=(
            Struct(datatype=0, data=1, bookend=0x77),
            [0, 1, 0x77],
        ),
        dump=Baseline(
            """
            +--------+----------+-------+-------+--------+
            | Offset | Access   | Value | Bytes | Format |
            +--------+----------+-------+-------+--------+
            |        |          |       |       | Struct |
            | 0      | datatype | 0     | 00    | uint8  |
            | 1      | data     | 1     | 01    | uint8  |
            | 2      | bookend  | 119   | 77    | uint8  |
            +--------+----------+-------+-------+--------+
            """
        ),
        excess=Baseline(
            """
            +--------+----------+----------------+-------+--------+
            | Offset | Access   | Value          | Bytes | Format |
            +--------+----------+----------------+-------+--------+
            |        |          |                |       | Struct |
            | 0      | datatype | 0              | 00    | uint8  |
            | 1      | data     | 1              | 01    | uint8  |
            | 2      | bookend  | 119            | 77    | uint8  |
            +--------+----------+----------------+-------+--------+
            | 3      |          | <excess bytes> | 99    |        |
            +--------+----------+----------------+-------+--------+

            ExcessMemoryError occurred during unpack operation:

            1 unconsumed bytes
            """
        ),
        shortage=Baseline(
            """
            +--------+----------+----------------------+-------+--------+
            | Offset | Access   | Value                | Bytes | Format |
            +--------+----------+----------------------+-------+--------+
            |        |          |                      |       | Struct |
            | 0      | datatype | 0                    | 00    | uint8  |
            | 1      | data     | 1                    | 01    | uint8  |
            |        | bookend  | <insufficient bytes> |       | uint8  |
            +--------+----------+----------------------+-------+--------+

            InsufficientMemoryError occurred during unpack operation:

            1 too few bytes to unpack 'uint8' (1 needed, only 0 available)
            """
        ),
        implementation=Baseline(
            """
            def __init__(self, *, datatype: int, data: int, bookend: int) -> None:
                self[:] = (datatype, data, bookend)

            @datatype.getter
            def datatype(self) -> int:
                return self[0]

            @datatype.setter
            def datatype(self, value: int) -> None:
                self[0] = value

            @data.getter
            def data(self) -> int:
                return self[1]

            @data.setter
            def data(self, value: int) -> None:
                self[1] = value

            @bookend.getter
            def bookend(self) -> int:
                return self[2]

            @bookend.setter
            def bookend(self, value: int) -> None:
                self[2] = value

            @classmethod
            def __pack__(cls, value, pieces: List[bytes], dump: Optional[Record] = None) -> None:
                (m_datatype, m_data, m_bookend) = value

                if dump is None:
                    uint8.__pack__(m_datatype, pieces, dump)

                    data_fmt = cls.data.fmt(m_datatype)
                    data_fmt.__pack__(m_data, pieces, dump)

                    uint8.__pack__(m_bookend, pieces, dump)

                else:
                    datatype_dump = dump.add_record(access="datatype", fmt=uint8)
                    uint8.__pack__(m_datatype, pieces, datatype_dump)

                    data_fmt = cls.data.fmt(m_datatype)
                    data_dump = dump.add_record(access="data", fmt=data_fmt)
                    data_fmt.__pack__(m_data, pieces, data_dump)

                    bookend_dump = dump.add_record(access="bookend", fmt=uint8)
                    uint8.__pack__(m_bookend, pieces, bookend_dump)

            @classmethod
            def __unpack__(cls, buffer: bytes, offset: int, dump: Optional[Record] = None) -> Tuple["Struct", int]:
                structure = list.__new__(cls)

                if dump is None:
                    m_datatype, offset = uint8.__unpack__(buffer, offset, dump)

                    data_fmt = cls.data.fmt(m_datatype)
                    m_data, offset = data_fmt.__unpack__(buffer, offset, dump)

                    m_bookend, offset = uint8.__unpack__(buffer, offset, dump)

                else:
                    datatype_dump = dump.add_record(access="datatype", fmt=uint8)
                    m_datatype, offset = uint8.__unpack__(buffer, offset, datatype_dump)

                    data_fmt = cls.data.fmt(m_datatype)
                    data_dump = dump.add_record(access="data", fmt=data_fmt)
                    m_data, offset = data_fmt.__unpack__(buffer, offset, data_dump)

                    bookend_dump = dump.add_record(access="bookend", fmt=uint8)
                    m_bookend, offset = uint8.__unpack__(buffer, offset, bookend_dump)

                structure[:] = (m_datatype, m_data, m_bookend)

                return structure, offset

            __eq__ = list.__eq__

            __ne__ = list.__ne__

            def __repr__(self) -> str:
                try:
                    return f"{type(self).__name__}(datatype={self.datatype!r}, data={self.data!r}, bookend={self.bookend!r})"
                except Exception:
                    return f"{type(self).__name__}()"

            """
        ),
    )


class TestMethod(Case):

    """Factory passed half baked structure instance (factory is a simple method)."""

    class Struct(Structure):
        def datatype_fmt(self):
            mapping = {0: uint8, 1: uint16}
            return mapping[self[0]]

        datatype: int = member(fmt=uint8)
        data: int = member(fmt=datatype_fmt)
        bookend: int = member(fmt=uint8)

    data = CaseData(
        fmt=Struct,
        bindata=bytes.fromhex("000177"),
        nbytes=None,
        values=(
            Struct(datatype=0, data=1, bookend=0x77),
            [0, 1, 0x77],
        ),
        dump=Baseline(
            """
            +--------+----------+-------+-------+--------+
            | Offset | Access   | Value | Bytes | Format |
            +--------+----------+-------+-------+--------+
            |        |          |       |       | Struct |
            | 0      | datatype | 0     | 00    | uint8  |
            | 1      | data     | 1     | 01    | uint8  |
            | 2      | bookend  | 119   | 77    | uint8  |
            +--------+----------+-------+-------+--------+
            """
        ),
        excess=Baseline(
            """
            +--------+----------+----------------+-------+--------+
            | Offset | Access   | Value          | Bytes | Format |
            +--------+----------+----------------+-------+--------+
            |        |          |                |       | Struct |
            | 0      | datatype | 0              | 00    | uint8  |
            | 1      | data     | 1              | 01    | uint8  |
            | 2      | bookend  | 119            | 77    | uint8  |
            +--------+----------+----------------+-------+--------+
            | 3      |          | <excess bytes> | 99    |        |
            +--------+----------+----------------+-------+--------+

            ExcessMemoryError occurred during unpack operation:

            1 unconsumed bytes
            """
        ),
        shortage=Baseline(
            """
            +--------+----------+----------------------+-------+--------+
            | Offset | Access   | Value                | Bytes | Format |
            +--------+----------+----------------------+-------+--------+
            |        |          |                      |       | Struct |
            | 0      | datatype | 0                    | 00    | uint8  |
            | 1      | data     | 1                    | 01    | uint8  |
            |        | bookend  | <insufficient bytes> |       | uint8  |
            +--------+----------+----------------------+-------+--------+

            InsufficientMemoryError occurred during unpack operation:

            1 too few bytes to unpack 'uint8' (1 needed, only 0 available)
            """
        ),
        implementation=Baseline(
            """
            def __init__(self, *, datatype: int, data: int, bookend: int) -> None:
                self[:] = (datatype, data, bookend)

            @datatype.getter
            def datatype(self) -> int:
                return self[0]

            @datatype.setter
            def datatype(self, value: int) -> None:
                self[0] = value

            @data.getter
            def data(self) -> int:
                return self[1]

            @data.setter
            def data(self, value: int) -> None:
                self[1] = value

            @bookend.getter
            def bookend(self) -> int:
                return self[2]

            @bookend.setter
            def bookend(self, value: int) -> None:
                self[2] = value

            @classmethod
            def __pack__(cls, value, pieces: List[bytes], dump: Optional[Record] = None) -> None:
                (m_datatype, m_data, m_bookend) = value

                if dump is None:
                    uint8.__pack__(m_datatype, pieces, dump)

                    data_fmt = cls.data.fmt(value)
                    data_fmt.__pack__(m_data, pieces, dump)

                    uint8.__pack__(m_bookend, pieces, dump)

                else:
                    datatype_dump = dump.add_record(access="datatype", fmt=uint8)
                    uint8.__pack__(m_datatype, pieces, datatype_dump)

                    data_fmt = cls.data.fmt(value)
                    data_dump = dump.add_record(access="data", fmt=data_fmt)
                    data_fmt.__pack__(m_data, pieces, data_dump)

                    bookend_dump = dump.add_record(access="bookend", fmt=uint8)
                    uint8.__pack__(m_bookend, pieces, bookend_dump)

            @classmethod
            def __unpack__(cls, buffer: bytes, offset: int, dump: Optional[Record] = None) -> Tuple["Struct", int]:
                structure = list.__new__(cls)
                add_member = structure.append

                if dump is None:
                    m_datatype, offset = uint8.__unpack__(buffer, offset, dump)
                    add_member(m_datatype)

                    data_fmt = cls.data.fmt(structure)
                    m_data, offset = data_fmt.__unpack__(buffer, offset, dump)
                    add_member(m_data)

                    m_bookend, offset = uint8.__unpack__(buffer, offset, dump)
                    add_member(m_bookend)

                else:
                    datatype_dump = dump.add_record(access="datatype", fmt=uint8)
                    m_datatype, offset = uint8.__unpack__(buffer, offset, datatype_dump)
                    add_member(m_datatype)

                    data_fmt = cls.data.fmt(structure)
                    data_dump = dump.add_record(access="data", fmt=data_fmt)
                    m_data, offset = data_fmt.__unpack__(buffer, offset, data_dump)
                    add_member(m_data)

                    bookend_dump = dump.add_record(access="bookend", fmt=uint8)
                    m_bookend, offset = uint8.__unpack__(buffer, offset, bookend_dump)
                    add_member(m_bookend)

                return structure, offset

            __eq__ = list.__eq__

            __ne__ = list.__ne__

            def __repr__(self) -> str:
                try:
                    return f"{type(self).__name__}(datatype={self.datatype!r}, data={self.data!r}, bookend={self.bookend!r})"
                except Exception:
                    return f"{type(self).__name__}()"

            """
        ),
    )


class TestProperty(Case):

    """Factory passed half baked structure instance (factory is a property method)."""

    class Struct(Structure):
        @property
        def datatype_fmt(self):
            mapping = {0: uint8, 1: uint16}
            return mapping[self[0]]

        datatype: int = member(fmt=uint8)
        data: int = member(fmt=datatype_fmt)
        bookend: int = member(fmt=uint8)

    data = CaseData(
        fmt=Struct,
        bindata=bytes.fromhex("000177"),
        nbytes=None,
        values=(
            Struct(datatype=0, data=1, bookend=0x77),
            [0, 1, 0x77],
        ),
        dump=Baseline(
            """
            +--------+----------+-------+-------+--------+
            | Offset | Access   | Value | Bytes | Format |
            +--------+----------+-------+-------+--------+
            |        |          |       |       | Struct |
            | 0      | datatype | 0     | 00    | uint8  |
            | 1      | data     | 1     | 01    | uint8  |
            | 2      | bookend  | 119   | 77    | uint8  |
            +--------+----------+-------+-------+--------+
            """
        ),
        excess=Baseline(
            """
            +--------+----------+----------------+-------+--------+
            | Offset | Access   | Value          | Bytes | Format |
            +--------+----------+----------------+-------+--------+
            |        |          |                |       | Struct |
            | 0      | datatype | 0              | 00    | uint8  |
            | 1      | data     | 1              | 01    | uint8  |
            | 2      | bookend  | 119            | 77    | uint8  |
            +--------+----------+----------------+-------+--------+
            | 3      |          | <excess bytes> | 99    |        |
            +--------+----------+----------------+-------+--------+

            ExcessMemoryError occurred during unpack operation:

            1 unconsumed bytes
            """
        ),
        shortage=Baseline(
            """
            +--------+----------+----------------------+-------+--------+
            | Offset | Access   | Value                | Bytes | Format |
            +--------+----------+----------------------+-------+--------+
            |        |          |                      |       | Struct |
            | 0      | datatype | 0                    | 00    | uint8  |
            | 1      | data     | 1                    | 01    | uint8  |
            |        | bookend  | <insufficient bytes> |       | uint8  |
            +--------+----------+----------------------+-------+--------+

            InsufficientMemoryError occurred during unpack operation:

            1 too few bytes to unpack 'uint8' (1 needed, only 0 available)
            """
        ),
        implementation=Baseline(
            """
            def __init__(self, *, datatype: int, data: int, bookend: int) -> None:
                self[:] = (datatype, data, bookend)

            @datatype.getter
            def datatype(self) -> int:
                return self[0]

            @datatype.setter
            def datatype(self, value: int) -> None:
                self[0] = value

            @data.getter
            def data(self) -> int:
                return self[1]

            @data.setter
            def data(self, value: int) -> None:
                self[1] = value

            @bookend.getter
            def bookend(self) -> int:
                return self[2]

            @bookend.setter
            def bookend(self, value: int) -> None:
                self[2] = value

            @classmethod
            def __pack__(cls, value, pieces: List[bytes], dump: Optional[Record] = None) -> None:
                (m_datatype, m_data, m_bookend) = value

                if dump is None:
                    uint8.__pack__(m_datatype, pieces, dump)

                    data_fmt = cls.data.fmt(value)
                    data_fmt.__pack__(m_data, pieces, dump)

                    uint8.__pack__(m_bookend, pieces, dump)

                else:
                    datatype_dump = dump.add_record(access="datatype", fmt=uint8)
                    uint8.__pack__(m_datatype, pieces, datatype_dump)

                    data_fmt = cls.data.fmt(value)
                    data_dump = dump.add_record(access="data", fmt=data_fmt)
                    data_fmt.__pack__(m_data, pieces, data_dump)

                    bookend_dump = dump.add_record(access="bookend", fmt=uint8)
                    uint8.__pack__(m_bookend, pieces, bookend_dump)

            @classmethod
            def __unpack__(cls, buffer: bytes, offset: int, dump: Optional[Record] = None) -> Tuple["Struct", int]:
                structure = list.__new__(cls)
                add_member = structure.append

                if dump is None:
                    m_datatype, offset = uint8.__unpack__(buffer, offset, dump)
                    add_member(m_datatype)

                    data_fmt = cls.data.fmt(structure)
                    m_data, offset = data_fmt.__unpack__(buffer, offset, dump)
                    add_member(m_data)

                    m_bookend, offset = uint8.__unpack__(buffer, offset, dump)
                    add_member(m_bookend)

                else:
                    datatype_dump = dump.add_record(access="datatype", fmt=uint8)
                    m_datatype, offset = uint8.__unpack__(buffer, offset, datatype_dump)
                    add_member(m_datatype)

                    data_fmt = cls.data.fmt(structure)
                    data_dump = dump.add_record(access="data", fmt=data_fmt)
                    m_data, offset = data_fmt.__unpack__(buffer, offset, data_dump)
                    add_member(m_data)

                    bookend_dump = dump.add_record(access="bookend", fmt=uint8)
                    m_bookend, offset = uint8.__unpack__(buffer, offset, bookend_dump)
                    add_member(m_bookend)

                return structure, offset

            __eq__ = list.__eq__

            __ne__ = list.__ne__

            def __repr__(self) -> str:
                try:
                    return f"{type(self).__name__}(datatype={self.datatype!r}, data={self.data!r}, bookend={self.bookend!r})"
                except Exception:
                    return f"{type(self).__name__}()"

            """
        ),
    )


class TestExceptions:

    """Test exception use cases."""

    def test_bad_key_reference(self):
        """Verify exception/message if Member gets an invalid fmt_arg."""
        with pytest.raises(TypeError) as trap:

            class BadRef(Structure):  # pylint: disable=unused-variable

                """Simple variably typed member with bad reference."""

                datatype: int = member(fmt=uint8)
                data: int = member(fmt_arg="junk", fmt={0: uint8}.__getitem__)

        expected = Baseline(
            """
            'fmt_arg' must be a structure 'member()'
            """
        )

        assert wrap_message(trap.value) == expected
