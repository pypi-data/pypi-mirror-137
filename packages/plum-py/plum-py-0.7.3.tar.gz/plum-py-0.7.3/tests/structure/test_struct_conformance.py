# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# Copyright 2021 Daniel Mark Gass, see __about__.py for license information.
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
"""Test structure data store transform API conformance."""

# pylint: disable=unexpected-keyword-arg

from baseline import Baseline

from plum.conformance import Case, CaseData
from plum.littleendian import uint8, uint16
from plum.structure import Structure, member


class Custom(Structure):

    """Sample Structure class."""

    m0: int = member(fmt=uint8)
    m1: int = member(fmt=uint16)


class TestConformance(Case):

    """Test structure data store transform conformance."""

    data = CaseData(
        fmt=Custom,
        bindata=b"\x01\x02\x00",
        nbytes=3,
        values=(Custom(m0=1, m1=2), [1, 2], (1, 2)),
        dump=Baseline(
            """
            +--------+--------+-------+-------+--------+
            | Offset | Access | Value | Bytes | Format |
            +--------+--------+-------+-------+--------+
            |        |        |       |       | Custom |
            | 0      | m0     | 1     | 01    | uint8  |
            | 1      | m1     | 2     | 02 00 | uint16 |
            +--------+--------+-------+-------+--------+
            """
        ),
        excess=Baseline(
            """
            +--------+--------+----------------+-------+--------+
            | Offset | Access | Value          | Bytes | Format |
            +--------+--------+----------------+-------+--------+
            |        |        |                |       | Custom |
            | 0      | m0     | 1              | 01    | uint8  |
            | 1      | m1     | 2              | 02 00 | uint16 |
            +--------+--------+----------------+-------+--------+
            | 3      |        | <excess bytes> | 99    |        |
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
            |        |        |                      |       | Custom |
            | 0      | m0     | 1                    | 01    | uint8  |
            | 1      | m1     | <insufficient bytes> | 02    | uint16 |
            +--------+--------+----------------------+-------+--------+

            InsufficientMemoryError occurred during unpack operation:

            1 too few bytes to unpack 'uint16' (2 needed, only 1 available)
            """
        ),
        implementation=Baseline(
            """
            def __init__(self, *, m0: int, m1: int) -> None:
                self[:] = (m0, m1)

            @m0.getter
            def m0(self) -> int:
                return self[0]

            @m0.setter
            def m0(self, value: int) -> None:
                self[0] = value

            @m1.getter
            def m1(self) -> int:
                return self[1]

            @m1.setter
            def m1(self, value: int) -> None:
                self[1] = value

            @classmethod
            def __pack__(cls, value, pieces: List[bytes], dump: Optional[Record] = None) -> None:
                (m_m0, m_m1) = value

                if dump is None:
                    uint8.__pack__(m_m0, pieces, dump)

                    uint16.__pack__(m_m1, pieces, dump)

                else:
                    m0_dump = dump.add_record(access="m0", fmt=uint8)
                    uint8.__pack__(m_m0, pieces, m0_dump)

                    m1_dump = dump.add_record(access="m1", fmt=uint16)
                    uint16.__pack__(m_m1, pieces, m1_dump)

            @classmethod
            def __unpack__(cls, buffer: bytes, offset: int, dump: Optional[Record] = None) -> Tuple["Custom", int]:
                structure = list.__new__(cls)

                if dump is None:
                    m_m0, offset = uint8.__unpack__(buffer, offset, dump)

                    m_m1, offset = uint16.__unpack__(buffer, offset, dump)

                else:
                    m0_dump = dump.add_record(access="m0", fmt=uint8)
                    m_m0, offset = uint8.__unpack__(buffer, offset, m0_dump)

                    m1_dump = dump.add_record(access="m1", fmt=uint16)
                    m_m1, offset = uint16.__unpack__(buffer, offset, m1_dump)

                structure[:] = (m_m0, m_m1)

                return structure, offset

            __eq__ = list.__eq__

            __ne__ = list.__ne__

            def __repr__(self) -> str:
                try:
                    return f"{type(self).__name__}(m0={self.m0!r}, m1={self.m1!r})"
                except Exception:
                    return f"{type(self).__name__}()"

            """
        ),
    )
