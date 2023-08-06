# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# Copyright 2021 Daniel Mark Gass, see __about__.py for license information.
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
"""Test default factory function as default."""

from baseline import Baseline

from plum.conformance import Case, CaseData
from plum.littleendian import uint8
from plum.structure import Structure, member


class TestMethod(Case):

    """Factory passed half baked structure instance (factory is a simple method)."""

    class Struct(Structure):
        def data_default(self):
            mapping = {0: 0x10, 1: 0x20}
            return mapping[self[0]]

        prev: int = member(fmt=uint8)
        data: int = member(fmt=uint8, default=data_default)

    data = CaseData(
        fmt=Struct,
        bindata=bytes.fromhex("0010"),
        nbytes=2,
        values=(
            Struct(prev=0, data=0x10),
            Struct(prev=0),
            [0, 0x10],
        ),
        dump=Baseline(
            """
            +--------+--------+-------+-------+--------+
            | Offset | Access | Value | Bytes | Format |
            +--------+--------+-------+-------+--------+
            |        |        |       |       | Struct |
            | 0      | prev   | 0     | 00    | uint8  |
            | 1      | data   | 16    | 10    | uint8  |
            +--------+--------+-------+-------+--------+
            """
        ),
        excess=Baseline(
            """
            +--------+--------+----------------+-------+--------+
            | Offset | Access | Value          | Bytes | Format |
            +--------+--------+----------------+-------+--------+
            |        |        |                |       | Struct |
            | 0      | prev   | 0              | 00    | uint8  |
            | 1      | data   | 16             | 10    | uint8  |
            +--------+--------+----------------+-------+--------+
            | 2      |        | <excess bytes> | 99    |        |
            +--------+--------+----------------+-------+--------+

            ExcessMemoryError occurred during unpack operation:

            1 unconsumed bytes
            """
        ),
        shortage=Baseline(
            """
            +--------+--------+----------------------+-------+--------+
            | Offset | Access | Value                | Bytes | Format |
            +--------+--------+----------------------+-------+--------+
            |        |        |                      |       | Struct |
            | 0      | prev   | 0                    | 00    | uint8  |
            |        | data   | <insufficient bytes> |       | uint8  |
            +--------+--------+----------------------+-------+--------+

            InsufficientMemoryError occurred during unpack operation:

            1 too few bytes to unpack 'uint8' (1 needed, only 0 available)
            """
        ),
        implementation=Baseline(
            """
            def __init__(self, *, prev: int, data: Optional[int] = None) -> None:
                self[:] = (prev, data)

                if data is None:
                    self[1] = type(self).data.default(self)

            @prev.getter
            def prev(self) -> int:
                return self[0]

            @prev.setter
            def prev(self, value: int) -> None:
                self[0] = value

            @data.getter
            def data(self) -> int:
                return self[1]

            @data.setter
            def data(self, value: int) -> None:
                self[1] = value

            @classmethod
            def __pack__(cls, value, pieces: List[bytes], dump: Optional[Record] = None) -> None:
                (m_prev, m_data) = value

                if dump is None:
                    uint8.__pack__(m_prev, pieces, dump)

                    uint8.__pack__(m_data, pieces, dump)

                else:
                    prev_dump = dump.add_record(access="prev", fmt=uint8)
                    uint8.__pack__(m_prev, pieces, prev_dump)

                    data_dump = dump.add_record(access="data", fmt=uint8)
                    uint8.__pack__(m_data, pieces, data_dump)

            @classmethod
            def __unpack__(cls, buffer: bytes, offset: int, dump: Optional[Record] = None) -> Tuple["Struct", int]:
                structure = list.__new__(cls)

                if dump is None:
                    m_prev, offset = uint8.__unpack__(buffer, offset, dump)

                    m_data, offset = uint8.__unpack__(buffer, offset, dump)

                else:
                    prev_dump = dump.add_record(access="prev", fmt=uint8)
                    m_prev, offset = uint8.__unpack__(buffer, offset, prev_dump)

                    data_dump = dump.add_record(access="data", fmt=uint8)
                    m_data, offset = uint8.__unpack__(buffer, offset, data_dump)

                structure[:] = (m_prev, m_data)

                return structure, offset

            __eq__ = list.__eq__

            __ne__ = list.__ne__

            def __repr__(self) -> str:
                try:
                    return f"{type(self).__name__}(prev={self.prev!r}, data={self.data!r})"
                except Exception:
                    return f"{type(self).__name__}()"

            """
        ),
    )


class TestProperty(Case):

    """Factory passed half baked structure instance (factory is a property method)."""

    class Struct(Structure):
        @property
        def data_default(self):
            mapping = {0: 0x10, 1: 0x20}
            return mapping[self[0]]

        prev: int = member(fmt=uint8)
        data: int = member(fmt=uint8, default=data_default)

    data = CaseData(
        fmt=Struct,
        bindata=bytes.fromhex("0010"),
        nbytes=2,
        values=(
            Struct(prev=0, data=0x10),
            Struct(prev=0),
            [0, 0x10],
        ),
        dump=Baseline(
            """
            +--------+--------+-------+-------+--------+
            | Offset | Access | Value | Bytes | Format |
            +--------+--------+-------+-------+--------+
            |        |        |       |       | Struct |
            | 0      | prev   | 0     | 00    | uint8  |
            | 1      | data   | 16    | 10    | uint8  |
            +--------+--------+-------+-------+--------+
            """
        ),
        excess=Baseline(
            """
            +--------+--------+----------------+-------+--------+
            | Offset | Access | Value          | Bytes | Format |
            +--------+--------+----------------+-------+--------+
            |        |        |                |       | Struct |
            | 0      | prev   | 0              | 00    | uint8  |
            | 1      | data   | 16             | 10    | uint8  |
            +--------+--------+----------------+-------+--------+
            | 2      |        | <excess bytes> | 99    |        |
            +--------+--------+----------------+-------+--------+

            ExcessMemoryError occurred during unpack operation:

            1 unconsumed bytes
            """
        ),
        shortage=Baseline(
            """
            +--------+--------+----------------------+-------+--------+
            | Offset | Access | Value                | Bytes | Format |
            +--------+--------+----------------------+-------+--------+
            |        |        |                      |       | Struct |
            | 0      | prev   | 0                    | 00    | uint8  |
            |        | data   | <insufficient bytes> |       | uint8  |
            +--------+--------+----------------------+-------+--------+

            InsufficientMemoryError occurred during unpack operation:

            1 too few bytes to unpack 'uint8' (1 needed, only 0 available)
            """
        ),
        implementation=Baseline(
            """
            def __init__(self, *, prev: int, data: Optional[int] = None) -> None:
                self[:] = (prev, data)

                if data is None:
                    self[1] = type(self).data.default(self)

            @prev.getter
            def prev(self) -> int:
                return self[0]

            @prev.setter
            def prev(self, value: int) -> None:
                self[0] = value

            @data.getter
            def data(self) -> int:
                return self[1]

            @data.setter
            def data(self, value: int) -> None:
                self[1] = value

            @classmethod
            def __pack__(cls, value, pieces: List[bytes], dump: Optional[Record] = None) -> None:
                (m_prev, m_data) = value

                if dump is None:
                    uint8.__pack__(m_prev, pieces, dump)

                    uint8.__pack__(m_data, pieces, dump)

                else:
                    prev_dump = dump.add_record(access="prev", fmt=uint8)
                    uint8.__pack__(m_prev, pieces, prev_dump)

                    data_dump = dump.add_record(access="data", fmt=uint8)
                    uint8.__pack__(m_data, pieces, data_dump)

            @classmethod
            def __unpack__(cls, buffer: bytes, offset: int, dump: Optional[Record] = None) -> Tuple["Struct", int]:
                structure = list.__new__(cls)

                if dump is None:
                    m_prev, offset = uint8.__unpack__(buffer, offset, dump)

                    m_data, offset = uint8.__unpack__(buffer, offset, dump)

                else:
                    prev_dump = dump.add_record(access="prev", fmt=uint8)
                    m_prev, offset = uint8.__unpack__(buffer, offset, prev_dump)

                    data_dump = dump.add_record(access="data", fmt=uint8)
                    m_data, offset = uint8.__unpack__(buffer, offset, data_dump)

                structure[:] = (m_prev, m_data)

                return structure, offset

            __eq__ = list.__eq__

            __ne__ = list.__ne__

            def __repr__(self) -> str:
                try:
                    return f"{type(self).__name__}(prev={self.prev!r}, data={self.data!r})"
                except Exception:
                    return f"{type(self).__name__}()"

            """
        ),
    )
