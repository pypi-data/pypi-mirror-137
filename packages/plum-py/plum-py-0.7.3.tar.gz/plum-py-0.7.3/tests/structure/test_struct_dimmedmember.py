# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# Copyright 2021 Daniel Mark Gass, see __about__.py for license information.
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
"""Test dimmed_member() support of cls factory."""

import sys
from enum import IntEnum

import pytest

from baseline import Baseline

from plum.array import ArrayX
from plum.conformance import Case, CaseData, wrap_message
from plum.enum import EnumX
from plum.littleendian import uint8, uint16
from plum.structure import Structure, dimmed_member, member

uint8array = ArrayX("uint8array", fmt=uint8)
uint16array = ArrayX("uint16array", fmt=uint16)


class DataType(IntEnum):

    """Array type."""

    UINT8 = 0
    UINT16 = 1


datatype = EnumX("datatype", DataType, nbytes=1, byteorder="big", signed=False)


array_map = {
    DataType.UINT8: uint8array,
    DataType.UINT16: uint16array,
}


def _get_array_cls(parent):
    return array_map[parent[0]]


def _get_data_type(parent):
    if max(parent[2]) < 256:
        cls = DataType.UINT8
    else:
        cls = DataType.UINT16
    return cls


class TestSimpleSingleDim(Case):

    """Test dimmed member has single dim."""

    class SampleStruct(Structure):

        data_len: int = member(fmt=uint8)
        data: list = dimmed_member(dims=data_len, fmt=uint8array)
        bookend: int = member(fmt=uint8)

    data = CaseData(
        fmt=SampleStruct,
        bindata=bytes.fromhex("040001020377"),
        nbytes=None,
        values=(
            SampleStruct(data_len=4, data=[0, 1, 2, 3], bookend=0x77),
            [4, [0, 1, 2, 3], 0x77],
        ),
        dump=Baseline(
            """
            +--------+----------+-------+-------+--------------+
            | Offset | Access   | Value | Bytes | Format       |
            +--------+----------+-------+-------+--------------+
            |        |          |       |       | SampleStruct |
            | 0      | data_len | 4     | 04    | uint8        |
            |        | data     |       |       | uint8array   |
            | 1      |   [0]    | 0     | 00    | uint8        |
            | 2      |   [1]    | 1     | 01    | uint8        |
            | 3      |   [2]    | 2     | 02    | uint8        |
            | 4      |   [3]    | 3     | 03    | uint8        |
            | 5      | bookend  | 119   | 77    | uint8        |
            +--------+----------+-------+-------+--------------+
            """
        ),
        excess=Baseline(
            """
            +--------+----------+----------------+-------+--------------+
            | Offset | Access   | Value          | Bytes | Format       |
            +--------+----------+----------------+-------+--------------+
            |        |          |                |       | SampleStruct |
            | 0      | data_len | 4              | 04    | uint8        |
            |        | data     |                |       | uint8array   |
            | 1      |   [0]    | 0              | 00    | uint8        |
            | 2      |   [1]    | 1              | 01    | uint8        |
            | 3      |   [2]    | 2              | 02    | uint8        |
            | 4      |   [3]    | 3              | 03    | uint8        |
            | 5      | bookend  | 119            | 77    | uint8        |
            +--------+----------+----------------+-------+--------------+
            | 6      |          | <excess bytes> | 99    |              |
            +--------+----------+----------------+-------+--------------+

            ExcessMemoryError occurred during unpack operation:

            1 unconsumed bytes
            """
        ),
        shortage=Baseline(
            """
            +--------+----------+----------------------+-------+--------------+
            | Offset | Access   | Value                | Bytes | Format       |
            +--------+----------+----------------------+-------+--------------+
            |        |          |                      |       | SampleStruct |
            | 0      | data_len | 4                    | 04    | uint8        |
            |        | data     |                      |       | uint8array   |
            | 1      |   [0]    | 0                    | 00    | uint8        |
            | 2      |   [1]    | 1                    | 01    | uint8        |
            | 3      |   [2]    | 2                    | 02    | uint8        |
            | 4      |   [3]    | 3                    | 03    | uint8        |
            |        | bookend  | <insufficient bytes> |       | uint8        |
            +--------+----------+----------------------+-------+--------------+

            InsufficientMemoryError occurred during unpack operation:

            1 too few bytes to unpack 'uint8' (1 needed, only 0 available)
            """
        ),
        implementation=Baseline(
            """
            def __init__(self, *, data_len: int, data: list, bookend: int) -> None:
                self[:] = (data_len, data, bookend)

            @data_len.getter
            def data_len(self) -> int:
                return self[0]

            @data_len.setter
            def data_len(self, value: int) -> None:
                self[0] = value

            @data.getter
            def data(self) -> list:
                return self[1]

            @data.setter
            def data(self, value: list) -> None:
                self[1] = value

            @bookend.getter
            def bookend(self) -> int:
                return self[2]

            @bookend.setter
            def bookend(self, value: int) -> None:
                self[2] = value

            @classmethod
            def __pack__(cls, value, pieces: List[bytes], dump: Optional[Record] = None) -> None:
                (m_data_len, m_data, m_bookend) = value

                if dump is None:
                    uint8.__pack__(m_data_len, pieces, dump)

                    uint8array.__pack__(m_data, pieces, dump, dims=(m_data_len, ))

                    uint8.__pack__(m_bookend, pieces, dump)

                else:
                    data_len_dump = dump.add_record(access="data_len", fmt=uint8)
                    uint8.__pack__(m_data_len, pieces, data_len_dump)

                    data_dump = dump.add_record(access="data", fmt=uint8array)
                    uint8array.__pack__(m_data, pieces, data_dump, dims=(m_data_len, ))

                    bookend_dump = dump.add_record(access="bookend", fmt=uint8)
                    uint8.__pack__(m_bookend, pieces, bookend_dump)

            @classmethod
            def __unpack__(cls, buffer: bytes, offset: int, dump: Optional[Record] = None) -> Tuple["SampleStruct", int]:
                structure = list.__new__(cls)

                if dump is None:
                    m_data_len, offset = uint8.__unpack__(buffer, offset, dump)

                    m_data, offset = uint8array.__unpack__(buffer, offset, dump, dims=(m_data_len, ))

                    m_bookend, offset = uint8.__unpack__(buffer, offset, dump)

                else:
                    data_len_dump = dump.add_record(access="data_len", fmt=uint8)
                    m_data_len, offset = uint8.__unpack__(buffer, offset, data_len_dump)

                    data_dump = dump.add_record(access="data", fmt=uint8array)
                    m_data, offset = uint8array.__unpack__(buffer, offset, data_dump, dims=(m_data_len, ))

                    bookend_dump = dump.add_record(access="bookend", fmt=uint8)
                    m_bookend, offset = uint8.__unpack__(buffer, offset, bookend_dump)

                structure[:] = (m_data_len, m_data, m_bookend)

                return structure, offset

            __eq__ = list.__eq__

            __ne__ = list.__ne__

            def __repr__(self) -> str:
                try:
                    return f"{type(self).__name__}(data_len={self.data_len!r}, data={self.data!r}, bookend={self.bookend!r})"
                except Exception:
                    return f"{type(self).__name__}()"

            """
        ),
    )


class TestTypeFactorySingleDim(Case):

    """Test dimmed member has single dim and variable type."""

    class SampleStruct(Structure):

        data_type: int = member(fmt=datatype, default=_get_data_type)
        data_len: int = member(fmt=uint8, compute=True)
        data: list = dimmed_member(dims=data_len, fmt=_get_array_cls)
        bookend: int = member(fmt=uint8)

    data = CaseData(
        fmt=SampleStruct,
        bindata=bytes.fromhex("00040001020377"),
        nbytes=None,
        values=(
            SampleStruct(
                data_type=DataType.UINT8, data_len=4, data=[0, 1, 2, 3], bookend=0x77
            ),
            SampleStruct(data=[0, 1, 2, 3], bookend=0x77),
            [DataType.UINT8, 4, [0, 1, 2, 3], 0x77],
        ),
        dump=Baseline(
            """
            +--------+-----------+----------------+-------+--------------+
            | Offset | Access    | Value          | Bytes | Format       |
            +--------+-----------+----------------+-------+--------------+
            |        |           |                |       | SampleStruct |
            | 0      | data_type | DataType.UINT8 | 00    | datatype     |
            | 1      | data_len  | 4              | 04    | uint8        |
            |        | data      |                |       | uint8array   |
            | 2      |   [0]     | 0              | 00    | uint8        |
            | 3      |   [1]     | 1              | 01    | uint8        |
            | 4      |   [2]     | 2              | 02    | uint8        |
            | 5      |   [3]     | 3              | 03    | uint8        |
            | 6      | bookend   | 119            | 77    | uint8        |
            +--------+-----------+----------------+-------+--------------+
            """
        ),
        excess=Baseline(
            """
            +--------+-----------+----------------+-------+--------------+
            | Offset | Access    | Value          | Bytes | Format       |
            +--------+-----------+----------------+-------+--------------+
            |        |           |                |       | SampleStruct |
            | 0      | data_type | DataType.UINT8 | 00    | datatype     |
            | 1      | data_len  | 4              | 04    | uint8        |
            |        | data      |                |       | uint8array   |
            | 2      |   [0]     | 0              | 00    | uint8        |
            | 3      |   [1]     | 1              | 01    | uint8        |
            | 4      |   [2]     | 2              | 02    | uint8        |
            | 5      |   [3]     | 3              | 03    | uint8        |
            | 6      | bookend   | 119            | 77    | uint8        |
            +--------+-----------+----------------+-------+--------------+
            | 7      |           | <excess bytes> | 99    |              |
            +--------+-----------+----------------+-------+--------------+

            ExcessMemoryError occurred during unpack operation:

            1 unconsumed bytes
            """
        ),
        shortage=Baseline(
            """
            +--------+-----------+----------------------+-------+--------------+
            | Offset | Access    | Value                | Bytes | Format       |
            +--------+-----------+----------------------+-------+--------------+
            |        |           |                      |       | SampleStruct |
            | 0      | data_type | DataType.UINT8       | 00    | datatype     |
            | 1      | data_len  | 4                    | 04    | uint8        |
            |        | data      |                      |       | uint8array   |
            | 2      |   [0]     | 0                    | 00    | uint8        |
            | 3      |   [1]     | 1                    | 01    | uint8        |
            | 4      |   [2]     | 2                    | 02    | uint8        |
            | 5      |   [3]     | 3                    | 03    | uint8        |
            |        | bookend   | <insufficient bytes> |       | uint8        |
            +--------+-----------+----------------------+-------+--------------+

            InsufficientMemoryError occurred during unpack operation:

            1 too few bytes to unpack 'uint8' (1 needed, only 0 available)
            """
        ),
        implementation=Baseline(
            """
            def __init__(self, *, data_type: Optional[int] = None, data_len: Optional[int] = None, data: list, bookend: int) -> None:
                if data_len is None:
                    data_len = len(data)

                self[:] = (data_type, data_len, data, bookend)

                if data_type is None:
                    self[0] = type(self).data_type.default(self)

            @data_type.getter
            def data_type(self) -> int:
                return self[0]

            @data_type.setter
            def data_type(self, value: int) -> None:
                self[0] = value

            @data_len.getter
            def data_len(self) -> int:
                return self[1]

            @data_len.setter
            def data_len(self, value: int) -> None:
                self[1] = value

            @data.getter
            def data(self) -> list:
                return self[2]

            @data.setter
            def data(self, value: list) -> None:
                self[1] = len(value)  # update 'data_len' member
                self[2] = value

            @bookend.getter
            def bookend(self) -> int:
                return self[3]

            @bookend.setter
            def bookend(self, value: int) -> None:
                self[3] = value

            @classmethod
            def __pack__(cls, value, pieces: List[bytes], dump: Optional[Record] = None) -> None:
                (m_data_type, m_data_len, m_data, m_bookend) = value

                if dump is None:
                    datatype.__pack__(m_data_type, pieces, dump)

                    uint8.__pack__(m_data_len, pieces, dump)

                    data_fmt = cls.data.fmt(value)
                    data_fmt.__pack__(m_data, pieces, dump, dims=(m_data_len, ))

                    uint8.__pack__(m_bookend, pieces, dump)

                else:
                    data_type_dump = dump.add_record(access="data_type", fmt=datatype)
                    datatype.__pack__(m_data_type, pieces, data_type_dump)

                    data_len_dump = dump.add_record(access="data_len", fmt=uint8)
                    uint8.__pack__(m_data_len, pieces, data_len_dump)

                    data_fmt = cls.data.fmt(value)
                    data_dump = dump.add_record(access="data", fmt=data_fmt)
                    data_fmt.__pack__(m_data, pieces, data_dump, dims=(m_data_len, ))

                    bookend_dump = dump.add_record(access="bookend", fmt=uint8)
                    uint8.__pack__(m_bookend, pieces, bookend_dump)

            @classmethod
            def __unpack__(cls, buffer: bytes, offset: int, dump: Optional[Record] = None) -> Tuple["SampleStruct", int]:
                structure = list.__new__(cls)
                add_member = structure.append

                if dump is None:
                    m_data_type, offset = datatype.__unpack__(buffer, offset, dump)
                    add_member(m_data_type)

                    m_data_len, offset = uint8.__unpack__(buffer, offset, dump)
                    add_member(m_data_len)

                    data_fmt = cls.data.fmt(structure)
                    m_data, offset = data_fmt.__unpack__(buffer, offset, dump, dims=(m_data_len, ))
                    add_member(m_data)

                    m_bookend, offset = uint8.__unpack__(buffer, offset, dump)
                    add_member(m_bookend)

                else:
                    data_type_dump = dump.add_record(access="data_type", fmt=datatype)
                    m_data_type, offset = datatype.__unpack__(buffer, offset, data_type_dump)
                    add_member(m_data_type)

                    data_len_dump = dump.add_record(access="data_len", fmt=uint8)
                    m_data_len, offset = uint8.__unpack__(buffer, offset, data_len_dump)
                    add_member(m_data_len)

                    data_fmt = cls.data.fmt(structure)
                    data_dump = dump.add_record(access="data", fmt=data_fmt)
                    m_data, offset = data_fmt.__unpack__(buffer, offset, data_dump, dims=(m_data_len, ))
                    add_member(m_data)

                    bookend_dump = dump.add_record(access="bookend", fmt=uint8)
                    m_bookend, offset = uint8.__unpack__(buffer, offset, bookend_dump)
                    add_member(m_bookend)

                return structure, offset

            def __eq__(self, other: Any) -> bool:
                if isinstance(other, type(self)):
                    _s_data_type, _s_data_len, _s_data, _s_bookend = self
                    if _s_data_len is None:
                        _s_data_type, _s_data_len, _s_data, _s_bookend = self.unpack(self.ipack())
                    _o_data_type, _o_data_len, _o_data, _o_bookend = other
                    if _o_data_len is None:
                        _o_data_type, _o_data_len, _o_data, _o_bookend = self.unpack(other.ipack())
                    return (_s_data_type, _s_data_len, _s_data, _s_bookend) == (_o_data_type, _o_data_len, _o_data, _o_bookend)
                else:
                    return list.__eq__(self, other)

            def __ne__(self, other: Any) -> bool:
                if isinstance(other, type(self)):
                    _s_data_type, _s_data_len, _s_data, _s_bookend = self
                    if _s_data_len is None:
                        _s_data_type, _s_data_len, _s_data, _s_bookend = self.unpack(self.ipack())
                    _o_data_type, _o_data_len, _o_data, _o_bookend = other
                    if _o_data_len is None:
                        _o_data_type, _o_data_len, _o_data, _o_bookend = self.unpack(other.ipack())
                    return (_s_data_type, _s_data_len, _s_data, _s_bookend) != (_o_data_type, _o_data_len, _o_data, _o_bookend)
                else:
                    return list.__ne__(self, other)

            def __repr__(self) -> str:
                try:
                    return f"{type(self).__name__}(data_type={str(self.data_type)}, data_len={self.data_len!r}, data={self.data!r}, bookend={self.bookend!r})"
                except Exception:
                    return f"{type(self).__name__}()"

            """
        ),
    )


class TestTypeFactoryMultiDim(Case):

    """Test dimmed member has multipe dims and variable type."""

    class MultiDimStruct(Structure):

        data_type: int = member(fmt=datatype, default=lambda parent: DataType.UINT8)
        data_dims: list = member(fmt=ArrayX("dims", fmt=uint8, dims=(2,)), compute=True)
        data: list = dimmed_member(dims=data_dims, fmt=_get_array_cls)
        bookend: int = member(fmt=uint8)

    data = CaseData(
        fmt=MultiDimStruct,
        bindata=bytes.fromhex("0002020001020377"),
        nbytes=None,
        values=(
            MultiDimStruct(
                data_type=DataType.UINT8,
                data_dims=[2, 2],
                data=[[0, 1], [2, 3]],
                bookend=0x77,
            ),
            MultiDimStruct(data=[[0, 1], [2, 3]], bookend=0x77),
            [DataType.UINT8, [2, 2], [[0, 1], [2, 3]], 0x77],
        ),
        dump=Baseline(
            """
            +--------+-----------+----------------+-------+----------------+
            | Offset | Access    | Value          | Bytes | Format         |
            +--------+-----------+----------------+-------+----------------+
            |        |           |                |       | MultiDimStruct |
            | 0      | data_type | DataType.UINT8 | 00    | datatype       |
            |        | data_dims |                |       | dims           |
            | 1      |   [0]     | 2              | 02    | uint8          |
            | 2      |   [1]     | 2              | 02    | uint8          |
            |        | data      |                |       | uint8array     |
            |        |   [0]     |                |       |                |
            | 3      |     [0]   | 0              | 00    | uint8          |
            | 4      |     [1]   | 1              | 01    | uint8          |
            |        |   [1]     |                |       |                |
            | 5      |     [0]   | 2              | 02    | uint8          |
            | 6      |     [1]   | 3              | 03    | uint8          |
            | 7      | bookend   | 119            | 77    | uint8          |
            +--------+-----------+----------------+-------+----------------+
            """
        ),
        excess=Baseline(
            """
            +--------+-----------+----------------+-------+----------------+
            | Offset | Access    | Value          | Bytes | Format         |
            +--------+-----------+----------------+-------+----------------+
            |        |           |                |       | MultiDimStruct |
            | 0      | data_type | DataType.UINT8 | 00    | datatype       |
            |        | data_dims |                |       | dims           |
            | 1      |   [0]     | 2              | 02    | uint8          |
            | 2      |   [1]     | 2              | 02    | uint8          |
            |        | data      |                |       | uint8array     |
            |        |   [0]     |                |       |                |
            | 3      |     [0]   | 0              | 00    | uint8          |
            | 4      |     [1]   | 1              | 01    | uint8          |
            |        |   [1]     |                |       |                |
            | 5      |     [0]   | 2              | 02    | uint8          |
            | 6      |     [1]   | 3              | 03    | uint8          |
            | 7      | bookend   | 119            | 77    | uint8          |
            +--------+-----------+----------------+-------+----------------+
            | 8      |           | <excess bytes> | 99    |                |
            +--------+-----------+----------------+-------+----------------+

            ExcessMemoryError occurred during unpack operation:

            1 unconsumed bytes
            """
        ),
        shortage=Baseline(
            """
            +--------+-----------+----------------------+-------+----------------+
            | Offset | Access    | Value                | Bytes | Format         |
            +--------+-----------+----------------------+-------+----------------+
            |        |           |                      |       | MultiDimStruct |
            | 0      | data_type | DataType.UINT8       | 00    | datatype       |
            |        | data_dims |                      |       | dims           |
            | 1      |   [0]     | 2                    | 02    | uint8          |
            | 2      |   [1]     | 2                    | 02    | uint8          |
            |        | data      |                      |       | uint8array     |
            |        |   [0]     |                      |       |                |
            | 3      |     [0]   | 0                    | 00    | uint8          |
            | 4      |     [1]   | 1                    | 01    | uint8          |
            |        |   [1]     |                      |       |                |
            | 5      |     [0]   | 2                    | 02    | uint8          |
            | 6      |     [1]   | 3                    | 03    | uint8          |
            |        | bookend   | <insufficient bytes> |       | uint8          |
            +--------+-----------+----------------------+-------+----------------+

            InsufficientMemoryError occurred during unpack operation:

            1 too few bytes to unpack 'uint8' (1 needed, only 0 available)
            """
        ),
        implementation=Baseline(
            """
            def __init__(self, *, data_type: Optional[int] = None, data_dims: Optional[list] = None, data: list, bookend: int) -> None:
                if data_dims is None:
                    data_dims = list(type(self).data.compute_dims(data, 2))

                self[:] = (data_type, data_dims, data, bookend)

                if data_type is None:
                    self[0] = type(self).data_type.default(self)

            @data_type.getter
            def data_type(self) -> int:
                return self[0]

            @data_type.setter
            def data_type(self, value: int) -> None:
                self[0] = value

            @data_dims.getter
            def data_dims(self) -> list:
                return self[1]

            @data_dims.setter
            def data_dims(self, value: list) -> None:
                self[1] = value

            @data.getter
            def data(self) -> list:
                return self[2]

            @data.setter
            def data(self, value: list) -> None:
                self[1] = list(type(self).data.compute_dims(value, 2))  # update 'data_dims' member
                self[2] = value

            @bookend.getter
            def bookend(self) -> int:
                return self[3]

            @bookend.setter
            def bookend(self, value: int) -> None:
                self[3] = value

            @classmethod
            def __pack__(cls, value, pieces: List[bytes], dump: Optional[Record] = None) -> None:
                (m_data_type, m_data_dims, m_data, m_bookend) = value

                if dump is None:
                    datatype.__pack__(m_data_type, pieces, dump)

                    cls.data_dims.fmt.__pack__(m_data_dims, pieces, dump)

                    data_fmt = cls.data.fmt(value)
                    data_fmt.__pack__(m_data, pieces, dump, dims=m_data_dims)

                    uint8.__pack__(m_bookend, pieces, dump)

                else:
                    data_type_dump = dump.add_record(access="data_type", fmt=datatype)
                    datatype.__pack__(m_data_type, pieces, data_type_dump)

                    data_dims_dump = dump.add_record(access="data_dims", fmt=cls.data_dims.fmt)
                    cls.data_dims.fmt.__pack__(m_data_dims, pieces, data_dims_dump)

                    data_fmt = cls.data.fmt(value)
                    data_dump = dump.add_record(access="data", fmt=data_fmt)
                    data_fmt.__pack__(m_data, pieces, data_dump, dims=m_data_dims)

                    bookend_dump = dump.add_record(access="bookend", fmt=uint8)
                    uint8.__pack__(m_bookend, pieces, bookend_dump)

            @classmethod
            def __unpack__(cls, buffer: bytes, offset: int, dump: Optional[Record] = None) -> Tuple["MultiDimStruct", int]:
                structure = list.__new__(cls)
                add_member = structure.append

                if dump is None:
                    m_data_type, offset = datatype.__unpack__(buffer, offset, dump)
                    add_member(m_data_type)

                    m_data_dims, offset = cls.data_dims.fmt.__unpack__(buffer, offset, dump)
                    add_member(m_data_dims)

                    data_fmt = cls.data.fmt(structure)
                    m_data, offset = data_fmt.__unpack__(buffer, offset, dump, dims=m_data_dims)
                    add_member(m_data)

                    m_bookend, offset = uint8.__unpack__(buffer, offset, dump)
                    add_member(m_bookend)

                else:
                    data_type_dump = dump.add_record(access="data_type", fmt=datatype)
                    m_data_type, offset = datatype.__unpack__(buffer, offset, data_type_dump)
                    add_member(m_data_type)

                    data_dims_dump = dump.add_record(access="data_dims", fmt=cls.data_dims.fmt)
                    m_data_dims, offset = cls.data_dims.fmt.__unpack__(buffer, offset, data_dims_dump)
                    add_member(m_data_dims)

                    data_fmt = cls.data.fmt(structure)
                    data_dump = dump.add_record(access="data", fmt=data_fmt)
                    m_data, offset = data_fmt.__unpack__(buffer, offset, data_dump, dims=m_data_dims)
                    add_member(m_data)

                    bookend_dump = dump.add_record(access="bookend", fmt=uint8)
                    m_bookend, offset = uint8.__unpack__(buffer, offset, bookend_dump)
                    add_member(m_bookend)

                return structure, offset

            def __eq__(self, other: Any) -> bool:
                if isinstance(other, type(self)):
                    _s_data_type, _s_data_dims, _s_data, _s_bookend = self
                    if _s_data_dims is None:
                        _s_data_type, _s_data_dims, _s_data, _s_bookend = self.unpack(self.ipack())
                    _o_data_type, _o_data_dims, _o_data, _o_bookend = other
                    if _o_data_dims is None:
                        _o_data_type, _o_data_dims, _o_data, _o_bookend = self.unpack(other.ipack())
                    return (_s_data_type, _s_data_dims, _s_data, _s_bookend) == (_o_data_type, _o_data_dims, _o_data, _o_bookend)
                else:
                    return list.__eq__(self, other)

            def __ne__(self, other: Any) -> bool:
                if isinstance(other, type(self)):
                    _s_data_type, _s_data_dims, _s_data, _s_bookend = self
                    if _s_data_dims is None:
                        _s_data_type, _s_data_dims, _s_data, _s_bookend = self.unpack(self.ipack())
                    _o_data_type, _o_data_dims, _o_data, _o_bookend = other
                    if _o_data_dims is None:
                        _o_data_type, _o_data_dims, _o_data, _o_bookend = self.unpack(other.ipack())
                    return (_s_data_type, _s_data_dims, _s_data, _s_bookend) != (_o_data_type, _o_data_dims, _o_data, _o_bookend)
                else:
                    return list.__ne__(self, other)

            def __repr__(self) -> str:
                try:
                    return f"{type(self).__name__}(data_type={str(self.data_type)}, data_dims={self.data_dims!r}, data={self.data!r}, bookend={self.bookend!r})"
                except Exception:
                    return f"{type(self).__name__}()"

            """
        ),
    )

    expected_dump = Baseline(
        """
        +--------+---------------+----------------+-------+----------------+
        | Offset | Access        | Value          | Bytes | Format         |
        +--------+---------------+----------------+-------+----------------+
        |        |               |                |       | MultiDimStruct |
        | 0      | data_type [0] | DataType.UINT8 | 00    | datatype       |
        |        | data_dims [1] |                |       | dims           |
        | 1      |   [0]         | 2              | 02    | uint8          |
        | 2      |   [1]         | 2              | 02    | uint8          |
        |        | data [2]      |                |       | uint8array     |
        |        |   [0]         |                |       |                |
        | 3      |     [0]       | 0              | 00    | uint8          |
        | 4      |     [1]       | 1              | 01    | uint8          |
        |        |   [1]         |                |       |                |
        | 5      |     [0]       | 2              | 02    | uint8          |
        | 6      |     [1]       | 3              | 03    | uint8          |
        +--------+---------------+----------------+-------+----------------+
        """
    )


class TestExceptions:

    """Test exception use cases."""

    def test_bad_dims_member(self):
        """Verify exception/message if dimmed_member() gets bad dims member."""
        with pytest.raises(TypeError) as trap:

            class BadRef(Structure):  # pylint: disable=unused-variable

                """Simple sized array with bad reference."""

                count: int = member(fmt=uint8, compute=True)
                array: list = dimmed_member(fmt=ArrayX("array", fmt=uint8), dims="junk")
                bookend: uint8

        expected = Baseline(
            """
            invalid 'dims', must be a 'member()'
            """
        )

        assert wrap_message(trap.value) == expected

    def test_missing_array_member(self):
        """Verify exception/message if missing dimmed_member() definition."""
        with pytest.raises(TypeError) as trap:

            class BadRef(Structure):  # pylint: disable=unused-variable

                """Simple sized array with missing array member."""

                count: int = member(fmt=uint8, compute=True)

        expected = Baseline(
            """
            'count' member never associated with member used to compute it
            """
        )

        assert wrap_message(trap.value) == expected


class TestException:
    def test_dims_wrong_type(self):
        expected_message = Baseline(
            """
            'dims' dims member not an integer or array transform format
            """
        )

        with pytest.raises(TypeError) as trap:

            class Struct(Structure):  # pylint: disable=unused-variable
                dims = member(fmt=datatype, compute=True)
                array = dimmed_member(fmt=uint8array, dims=dims)

        assert str(trap.value) == expected_message


class TestSetter:
    def test_override(self):
        class Struct(Structure):
            dims = member(fmt=uint8, compute=True)
            array = dimmed_member(fmt=uint8array, dims=dims)

            @array.setter
            def array(self, value):
                # pylint: disable=unused-argument
                self[1] = [99]

        struct = Struct(dims=1, array=[0])
        struct.array = [1, 2, 3]
        assert struct.array == [99]

    def test_readonly(self):
        expected_message = Baseline(
            """
            can't set attribute 'array'
            """
        )

        class Struct(Structure):
            dims = member(fmt=uint8, compute=True)
            array = dimmed_member(fmt=uint8array, dims=dims, readonly=True)

        struct = Struct(dims=1, array=[0])

        with pytest.raises(AttributeError) as trap:
            struct.array = [1, 2, 3]

        actual_message = str(trap.value)

        if sys.version_info < (3, 10):
            actual_message += " 'array'"

        assert actual_message == expected_message
