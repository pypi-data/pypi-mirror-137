# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# Copyright 2021 Daniel Mark Gass, see __about__.py for license information.
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
"""Test BitFieldMember() member definition."""

# pylint: disable=too-many-lines

from enum import IntEnum
from baseline import Baseline

from plum.bigendian import uint8
from plum.conformance import Case, CaseData
from plum.structure import Structure, member, bitfield_member


class Pet(IntEnum):
    CAT = 0
    DOG = 1


class TestFirst(Case):

    """Bit fields are first members of structure."""

    class MyStruct(Structure, fieldorder="least_to_most"):

        m1: Pet = bitfield_member(typ=Pet, size=4)
        m2: int = bitfield_member(typ=int, size=4, default=1)
        m3: int = bitfield_member(typ=int, size=8, default=2)
        m4: int = member(fmt=uint8, default=0xFF)

    data = CaseData(
        fmt=MyStruct,
        bindata=b"\x21\x03\x04",
        nbytes=3,
        values=(
            MyStruct(m1=Pet.DOG, m2=2, m3=3, m4=4),
            [Pet.DOG, 2, 3, 4],
            (Pet.DOG, 2, 3, 4),
        ),
        dump=Baseline(
            """
            +---------+--------+---------+-------------------+----------+
            | Offset  | Access | Value   | Bytes             | Format   |
            +---------+--------+---------+-------------------+----------+
            |         |        |         |                   | MyStruct |
            | 0       |        | 801     | 21 03             |          |
            |  [0:4]  | m1     | Pet.DOG | ........ ....0001 | Pet      |
            |  [4:8]  | m2     | 2       | ........ 0010.... | int      |
            |  [8:16] | m3     | 3       | 00000011 ........ | int      |
            | 2       | m4     | 4       | 04                | uint8    |
            +---------+--------+---------+-------------------+----------+
            """
        ),
        excess=Baseline(
            """
            +---------+--------+----------------+-------------------+----------+
            | Offset  | Access | Value          | Bytes             | Format   |
            +---------+--------+----------------+-------------------+----------+
            |         |        |                |                   | MyStruct |
            | 0       |        | 801            | 21 03             |          |
            |  [0:4]  | m1     | Pet.DOG        | ........ ....0001 | Pet      |
            |  [4:8]  | m2     | 2              | ........ 0010.... | int      |
            |  [8:16] | m3     | 3              | 00000011 ........ | int      |
            | 2       | m4     | 4              | 04                | uint8    |
            +---------+--------+----------------+-------------------+----------+
            | 3       |        | <excess bytes> | 99                |          |
            +---------+--------+----------------+-------------------+----------+

            ExcessMemoryError occurred during unpack operation:

            1 unconsumed bytes
            """
        ),
        shortage=Baseline(
            """
            +---------+--------+----------------------+-------------------+----------+
            | Offset  | Access | Value                | Bytes             | Format   |
            +---------+--------+----------------------+-------------------+----------+
            |         |        |                      |                   | MyStruct |
            | 0       |        | 801                  | 21 03             |          |
            |  [0:4]  | m1     | Pet.DOG              | ........ ....0001 | Pet      |
            |  [4:8]  | m2     | 2                    | ........ 0010.... | int      |
            |  [8:16] | m3     | 3                    | 00000011 ........ | int      |
            |         | m4     | <insufficient bytes> |                   | uint8    |
            +---------+--------+----------------------+-------------------+----------+

            InsufficientMemoryError occurred during unpack operation:

            1 too few bytes to unpack 'uint8' (1 needed, only 0 available)
            """
        ),
        implementation=Baseline(
            """
            def __init__(self, *, m1: Pet, m2: int = 1, m3: int = 2, m4: int = 255) -> None:
                if not 0 <= m1 <= 15:
                   raise ValueError("'m1' out of range, 0 <= m1 <= 15")

                if not 0 <= m2 <= 15:
                   raise ValueError("'m2' out of range, 0 <= m2 <= 15")

                if not 0 <= m3 <= 255:
                   raise ValueError("'m3' out of range, 0 <= m3 <= 255")

                self[:] = (m1, m2, m3, m4)

            @m1.getter
            def m1(self) -> Pet:
                return self[0]

            @m1.setter
            def m1(self, value: Pet) -> None:
                self[0] = Pet(value)

            @m2.getter
            def m2(self) -> int:
                return self[1]

            @m2.setter
            def m2(self, value: int) -> None:
                if not 0 <= value <= 15:
                   raise ValueError("out of range, 0 <= value <= 15")
                self[1] = value

            @m3.getter
            def m3(self) -> int:
                return self[2]

            @m3.setter
            def m3(self, value: int) -> None:
                if not 0 <= value <= 255:
                   raise ValueError("out of range, 0 <= value <= 255")
                self[2] = value

            @m4.getter
            def m4(self) -> int:
                return self[3]

            @m4.setter
            def m4(self, value: int) -> None:
                self[3] = value

            @classmethod
            def __pack__(cls, value, pieces: List[bytes], dump: Optional[Record] = None) -> None:
                (m_m1, m_m2, m_m3, m_m4) = value

                if dump is None:
                    bitfields_0 = 0

                    bitfields_0 |= (bitfields_0 & -16) | (m_m1 & 0xf)

                    bitfields_0 |= (bitfields_0 & -241) | ((m_m2 & 0xf) << 4)

                    bitfields_0 |= (bitfields_0 & -65281) | ((m_m3 & 0xff) << 8)

                    pieces.append(bitfields_0.to_bytes(2, "little", signed=False))

                    uint8.__pack__(m_m4, pieces, dump)

                else:
                    bitfields_0_dump = dump.add_record()
                    bitfields_0 = 0

                    dump.add_record(access="m1", bits=(0, 4), value=m_m1, fmt=Pet)
                    bitfields_0 |= (bitfields_0 & -16) | (m_m1 & 0xf)

                    dump.add_record(access="m2", bits=(4, 4), value=m_m2, fmt=int)
                    bitfields_0 |= (bitfields_0 & -241) | ((m_m2 & 0xf) << 4)

                    dump.add_record(access="m3", bits=(8, 8), value=m_m3, fmt=int)
                    bitfields_0 |= (bitfields_0 & -65281) | ((m_m3 & 0xff) << 8)

                    pieces.append(bitfields_0.to_bytes(2, "little", signed=False))
                    bitfields_0_dump.value = str(bitfields_0)
                    bitfields_0_dump.memory = pieces[-1]

                    m4_dump = dump.add_record(access="m4", fmt=uint8)
                    uint8.__pack__(m_m4, pieces, m4_dump)

            @classmethod
            def __unpack__(cls, buffer: bytes, offset: int, dump: Optional[Record] = None) -> Tuple["MyStruct", int]:
                structure = list.__new__(cls)

                if dump is None:
                    bitfields_0, offset = cls.m1.__unpack__(buffer, offset, dump, "little", nbytes=2, signed=False)

                    m_m1 = (bitfields_0 >> 0) & 0xf
                    m_m1 = Pet(m_m1)

                    m_m2 = (bitfields_0 >> 4) & 0xf

                    m_m3 = (bitfields_0 >> 8) & 0xff

                    m_m4, offset = uint8.__unpack__(buffer, offset, dump)

                else:
                    bitfields_0_dump = dump.add_record()
                    bitfields_0, offset = cls.m1.__unpack__(buffer, offset, bitfields_0_dump, "little", nbytes=2, signed=False)

                    m_m1 = (bitfields_0 >> 0) & 0xf
                    m_m1 = Pet(m_m1)
                    dump.add_record(access="m1", bits=(0, 4), value=m_m1, fmt=Pet)

                    m_m2 = (bitfields_0 >> 4) & 0xf
                    dump.add_record(access="m2", bits=(4, 4), value=m_m2, fmt=int)

                    m_m3 = (bitfields_0 >> 8) & 0xff
                    dump.add_record(access="m3", bits=(8, 8), value=m_m3, fmt=int)

                    m4_dump = dump.add_record(access="m4", fmt=uint8)
                    m_m4, offset = uint8.__unpack__(buffer, offset, m4_dump)

                structure[:] = (m_m1, m_m2, m_m3, m_m4)

                return structure, offset

            __eq__ = list.__eq__

            __ne__ = list.__ne__

            def __repr__(self) -> str:
                try:
                    return f"{type(self).__name__}(m1={str(self.m1)}, m2={self.m2!r}, m3={self.m3!r}, m4={self.m4!r})"
                except Exception:
                    return f"{type(self).__name__}()"

            """
        ),
    )


class TestLast(Case):
    """Bit fields are last members of structure."""

    class MyStruct(Structure, fieldorder="least_to_most"):

        m0: int = member(fmt=uint8, default=0xFF)
        m1: int = bitfield_member(typ=int, size=4)
        m2: int = bitfield_member(typ=int, size=4, default=1)
        m3: int = bitfield_member(typ=int, size=8, default=2)

    data = CaseData(
        fmt=MyStruct,
        bindata=b"\x00\x21\x03",
        nbytes=3,
        values=(MyStruct(m0=0, m1=1, m2=2, m3=3), [0, 1, 2, 3], (0, 1, 2, 3)),
        dump=Baseline(
            """
            +---------+--------+-------+-------------------+----------+
            | Offset  | Access | Value | Bytes             | Format   |
            +---------+--------+-------+-------------------+----------+
            |         |        |       |                   | MyStruct |
            | 0       | m0     | 0     | 00                | uint8    |
            | 1       |        | 801   | 21 03             |          |
            |  [0:4]  | m1     | 1     | ........ ....0001 | int      |
            |  [4:8]  | m2     | 2     | ........ 0010.... | int      |
            |  [8:16] | m3     | 3     | 00000011 ........ | int      |
            +---------+--------+-------+-------------------+----------+
            """
        ),
        excess=Baseline(
            """
            +---------+--------+----------------+-------------------+----------+
            | Offset  | Access | Value          | Bytes             | Format   |
            +---------+--------+----------------+-------------------+----------+
            |         |        |                |                   | MyStruct |
            | 0       | m0     | 0              | 00                | uint8    |
            | 1       |        | 801            | 21 03             |          |
            |  [0:4]  | m1     | 1              | ........ ....0001 | int      |
            |  [4:8]  | m2     | 2              | ........ 0010.... | int      |
            |  [8:16] | m3     | 3              | 00000011 ........ | int      |
            +---------+--------+----------------+-------------------+----------+
            | 3       |        | <excess bytes> | 99                |          |
            +---------+--------+----------------+-------------------+----------+

            ExcessMemoryError occurred during unpack operation:

            1 unconsumed bytes
            """
        ),
        shortage=Baseline(
            """
            +--------+--------+----------------------+-------+----------+
            | Offset | Access | Value                | Bytes | Format   |
            +--------+--------+----------------------+-------+----------+
            |        |        |                      |       | MyStruct |
            | 0      | m0     | 0                    | 00    | uint8    |
            | 1      |        | <insufficient bytes> | 21    |          |
            +--------+--------+----------------------+-------+----------+

            InsufficientMemoryError occurred during unpack operation:

            1 too few bytes to unpack (2 needed, only 1 available)
            """
        ),
        implementation=Baseline(
            """
            def __init__(self, *, m0: int = 255, m1: int, m2: int = 1, m3: int = 2) -> None:
                if not 0 <= m1 <= 15:
                   raise ValueError("'m1' out of range, 0 <= m1 <= 15")

                if not 0 <= m2 <= 15:
                   raise ValueError("'m2' out of range, 0 <= m2 <= 15")

                if not 0 <= m3 <= 255:
                   raise ValueError("'m3' out of range, 0 <= m3 <= 255")

                self[:] = (m0, m1, m2, m3)

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
                if not 0 <= value <= 15:
                   raise ValueError("out of range, 0 <= value <= 15")
                self[1] = value

            @m2.getter
            def m2(self) -> int:
                return self[2]

            @m2.setter
            def m2(self, value: int) -> None:
                if not 0 <= value <= 15:
                   raise ValueError("out of range, 0 <= value <= 15")
                self[2] = value

            @m3.getter
            def m3(self) -> int:
                return self[3]

            @m3.setter
            def m3(self, value: int) -> None:
                if not 0 <= value <= 255:
                   raise ValueError("out of range, 0 <= value <= 255")
                self[3] = value

            @classmethod
            def __pack__(cls, value, pieces: List[bytes], dump: Optional[Record] = None) -> None:
                (m_m0, m_m1, m_m2, m_m3) = value

                if dump is None:
                    uint8.__pack__(m_m0, pieces, dump)

                    bitfields_0 = 0

                    bitfields_0 |= (bitfields_0 & -16) | (m_m1 & 0xf)

                    bitfields_0 |= (bitfields_0 & -241) | ((m_m2 & 0xf) << 4)

                    bitfields_0 |= (bitfields_0 & -65281) | ((m_m3 & 0xff) << 8)

                    pieces.append(bitfields_0.to_bytes(2, "little", signed=False))

                else:
                    m0_dump = dump.add_record(access="m0", fmt=uint8)
                    uint8.__pack__(m_m0, pieces, m0_dump)

                    bitfields_0_dump = dump.add_record()
                    bitfields_0 = 0

                    dump.add_record(access="m1", bits=(0, 4), value=m_m1, fmt=int)
                    bitfields_0 |= (bitfields_0 & -16) | (m_m1 & 0xf)

                    dump.add_record(access="m2", bits=(4, 4), value=m_m2, fmt=int)
                    bitfields_0 |= (bitfields_0 & -241) | ((m_m2 & 0xf) << 4)

                    dump.add_record(access="m3", bits=(8, 8), value=m_m3, fmt=int)
                    bitfields_0 |= (bitfields_0 & -65281) | ((m_m3 & 0xff) << 8)

                    pieces.append(bitfields_0.to_bytes(2, "little", signed=False))
                    bitfields_0_dump.value = str(bitfields_0)
                    bitfields_0_dump.memory = pieces[-1]

            @classmethod
            def __unpack__(cls, buffer: bytes, offset: int, dump: Optional[Record] = None) -> Tuple["MyStruct", int]:
                structure = list.__new__(cls)

                if dump is None:
                    m_m0, offset = uint8.__unpack__(buffer, offset, dump)

                    bitfields_0, offset = cls.m1.__unpack__(buffer, offset, dump, "little", nbytes=2, signed=False)

                    m_m1 = (bitfields_0 >> 0) & 0xf

                    m_m2 = (bitfields_0 >> 4) & 0xf

                    m_m3 = (bitfields_0 >> 8) & 0xff

                else:
                    m0_dump = dump.add_record(access="m0", fmt=uint8)
                    m_m0, offset = uint8.__unpack__(buffer, offset, m0_dump)

                    bitfields_0_dump = dump.add_record()
                    bitfields_0, offset = cls.m1.__unpack__(buffer, offset, bitfields_0_dump, "little", nbytes=2, signed=False)

                    m_m1 = (bitfields_0 >> 0) & 0xf
                    dump.add_record(access="m1", bits=(0, 4), value=m_m1, fmt=int)

                    m_m2 = (bitfields_0 >> 4) & 0xf
                    dump.add_record(access="m2", bits=(4, 4), value=m_m2, fmt=int)

                    m_m3 = (bitfields_0 >> 8) & 0xff
                    dump.add_record(access="m3", bits=(8, 8), value=m_m3, fmt=int)

                structure[:] = (m_m0, m_m1, m_m2, m_m3)

                return structure, offset

            __eq__ = list.__eq__

            __ne__ = list.__ne__

            def __repr__(self) -> str:
                try:
                    return f"{type(self).__name__}(m0={self.m0!r}, m1={self.m1!r}, m2={self.m2!r}, m3={self.m3!r})"
                except Exception:
                    return f"{type(self).__name__}()"

            """
        ),
    )


class TestMultiple(Case):

    """Many bit field groups in structure."""

    class MyStruct(Structure, fieldorder="least_to_most"):

        m0: int = bitfield_member(typ=int, size=4)
        m1: int = bitfield_member(typ=int, size=8)

        m2: int = member(fmt=uint8)

        m3: int = bitfield_member(typ=int, size=4)
        m4: int = bitfield_member(typ=int, size=4)

        m5: int = member(fmt=uint8)

        m6: int = bitfield_member(typ=int, size=4)
        m7: int = bitfield_member(typ=int, size=8)

    data = CaseData(
        fmt=MyStruct,
        bindata=b"\x10\x00\x02\x43\x05\x76\x00",
        nbytes=7,
        values=(
            MyStruct(m0=0, m1=1, m2=2, m3=3, m4=4, m5=5, m6=6, m7=7),
            [0, 1, 2, 3, 4, 5, 6, 7],
            (0, 1, 2, 3, 4, 5, 6, 7),
        ),
        dump=Baseline(
            """
            +---------+--------+-------+-------------------+----------+
            | Offset  | Access | Value | Bytes             | Format   |
            +---------+--------+-------+-------------------+----------+
            |         |        |       |                   | MyStruct |
            | 0       |        | 16    | 10 00             |          |
            |  [0:4]  | m0     | 0     | ........ ....0000 | int      |
            |  [4:12] | m1     | 1     | ....0000 0001.... | int      |
            | 2       | m2     | 2     | 02                | uint8    |
            | 3       |        | 67    | 43                |          |
            |  [0:4]  | m3     | 3     | ....0011          | int      |
            |  [4:8]  | m4     | 4     | 0100....          | int      |
            | 4       | m5     | 5     | 05                | uint8    |
            | 5       |        | 118   | 76 00             |          |
            |  [0:4]  | m6     | 6     | ........ ....0110 | int      |
            |  [4:12] | m7     | 7     | ....0000 0111.... | int      |
            +---------+--------+-------+-------------------+----------+
            """
        ),
        excess=Baseline(
            """
            +---------+--------+----------------+-------------------+----------+
            | Offset  | Access | Value          | Bytes             | Format   |
            +---------+--------+----------------+-------------------+----------+
            |         |        |                |                   | MyStruct |
            | 0       |        | 16             | 10 00             |          |
            |  [0:4]  | m0     | 0              | ........ ....0000 | int      |
            |  [4:12] | m1     | 1              | ....0000 0001.... | int      |
            | 2       | m2     | 2              | 02                | uint8    |
            | 3       |        | 67             | 43                |          |
            |  [0:4]  | m3     | 3              | ....0011          | int      |
            |  [4:8]  | m4     | 4              | 0100....          | int      |
            | 4       | m5     | 5              | 05                | uint8    |
            | 5       |        | 118            | 76 00             |          |
            |  [0:4]  | m6     | 6              | ........ ....0110 | int      |
            |  [4:12] | m7     | 7              | ....0000 0111.... | int      |
            +---------+--------+----------------+-------------------+----------+
            | 7       |        | <excess bytes> | 99                |          |
            +---------+--------+----------------+-------------------+----------+

            ExcessMemoryError occurred during unpack operation:

            1 unconsumed bytes
            """
        ),
        shortage=Baseline(
            """
            +---------+--------+----------------------+-------------------+----------+
            | Offset  | Access | Value                | Bytes             | Format   |
            +---------+--------+----------------------+-------------------+----------+
            |         |        |                      |                   | MyStruct |
            | 0       |        | 16                   | 10 00             |          |
            |  [0:4]  | m0     | 0                    | ........ ....0000 | int      |
            |  [4:12] | m1     | 1                    | ....0000 0001.... | int      |
            | 2       | m2     | 2                    | 02                | uint8    |
            | 3       |        | 67                   | 43                |          |
            |  [0:4]  | m3     | 3                    | ....0011          | int      |
            |  [4:8]  | m4     | 4                    | 0100....          | int      |
            | 4       | m5     | 5                    | 05                | uint8    |
            | 5       |        | <insufficient bytes> | 76                |          |
            +---------+--------+----------------------+-------------------+----------+

            InsufficientMemoryError occurred during unpack operation:

            1 too few bytes to unpack (2 needed, only 1 available)
            """
        ),
        implementation=Baseline(
            """
            def __init__(self, *, m0: int, m1: int, m2: int, m3: int, m4: int, m5: int, m6: int, m7: int) -> None:
                if not 0 <= m0 <= 15:
                   raise ValueError("'m0' out of range, 0 <= m0 <= 15")

                if not 0 <= m1 <= 255:
                   raise ValueError("'m1' out of range, 0 <= m1 <= 255")

                if not 0 <= m3 <= 15:
                   raise ValueError("'m3' out of range, 0 <= m3 <= 15")

                if not 0 <= m4 <= 15:
                   raise ValueError("'m4' out of range, 0 <= m4 <= 15")

                if not 0 <= m6 <= 15:
                   raise ValueError("'m6' out of range, 0 <= m6 <= 15")

                if not 0 <= m7 <= 255:
                   raise ValueError("'m7' out of range, 0 <= m7 <= 255")

                self[:] = (m0, m1, m2, m3, m4, m5, m6, m7)

            @m0.getter
            def m0(self) -> int:
                return self[0]

            @m0.setter
            def m0(self, value: int) -> None:
                if not 0 <= value <= 15:
                   raise ValueError("out of range, 0 <= value <= 15")
                self[0] = value

            @m1.getter
            def m1(self) -> int:
                return self[1]

            @m1.setter
            def m1(self, value: int) -> None:
                if not 0 <= value <= 255:
                   raise ValueError("out of range, 0 <= value <= 255")
                self[1] = value

            @m2.getter
            def m2(self) -> int:
                return self[2]

            @m2.setter
            def m2(self, value: int) -> None:
                self[2] = value

            @m3.getter
            def m3(self) -> int:
                return self[3]

            @m3.setter
            def m3(self, value: int) -> None:
                if not 0 <= value <= 15:
                   raise ValueError("out of range, 0 <= value <= 15")
                self[3] = value

            @m4.getter
            def m4(self) -> int:
                return self[4]

            @m4.setter
            def m4(self, value: int) -> None:
                if not 0 <= value <= 15:
                   raise ValueError("out of range, 0 <= value <= 15")
                self[4] = value

            @m5.getter
            def m5(self) -> int:
                return self[5]

            @m5.setter
            def m5(self, value: int) -> None:
                self[5] = value

            @m6.getter
            def m6(self) -> int:
                return self[6]

            @m6.setter
            def m6(self, value: int) -> None:
                if not 0 <= value <= 15:
                   raise ValueError("out of range, 0 <= value <= 15")
                self[6] = value

            @m7.getter
            def m7(self) -> int:
                return self[7]

            @m7.setter
            def m7(self, value: int) -> None:
                if not 0 <= value <= 255:
                   raise ValueError("out of range, 0 <= value <= 255")
                self[7] = value

            @classmethod
            def __pack__(cls, value, pieces: List[bytes], dump: Optional[Record] = None) -> None:
                (m_m0, m_m1, m_m2, m_m3, m_m4, m_m5, m_m6, m_m7) = value

                if dump is None:
                    bitfields_0 = 0

                    bitfields_0 |= (bitfields_0 & -16) | (m_m0 & 0xf)

                    bitfields_0 |= (bitfields_0 & -4081) | ((m_m1 & 0xff) << 4)

                    pieces.append(bitfields_0.to_bytes(2, "little", signed=False))

                    uint8.__pack__(m_m2, pieces, dump)

                    bitfields_1 = 0

                    bitfields_1 |= (bitfields_1 & -16) | (m_m3 & 0xf)

                    bitfields_1 |= (bitfields_1 & -241) | ((m_m4 & 0xf) << 4)

                    pieces.append(bitfields_1.to_bytes(1, "little", signed=False))

                    uint8.__pack__(m_m5, pieces, dump)

                    bitfields_2 = 0

                    bitfields_2 |= (bitfields_2 & -16) | (m_m6 & 0xf)

                    bitfields_2 |= (bitfields_2 & -4081) | ((m_m7 & 0xff) << 4)

                    pieces.append(bitfields_2.to_bytes(2, "little", signed=False))

                else:
                    bitfields_0_dump = dump.add_record()
                    bitfields_0 = 0

                    dump.add_record(access="m0", bits=(0, 4), value=m_m0, fmt=int)
                    bitfields_0 |= (bitfields_0 & -16) | (m_m0 & 0xf)

                    dump.add_record(access="m1", bits=(4, 8), value=m_m1, fmt=int)
                    bitfields_0 |= (bitfields_0 & -4081) | ((m_m1 & 0xff) << 4)

                    pieces.append(bitfields_0.to_bytes(2, "little", signed=False))
                    bitfields_0_dump.value = str(bitfields_0)
                    bitfields_0_dump.memory = pieces[-1]

                    m2_dump = dump.add_record(access="m2", fmt=uint8)
                    uint8.__pack__(m_m2, pieces, m2_dump)

                    bitfields_1_dump = dump.add_record()
                    bitfields_1 = 0

                    dump.add_record(access="m3", bits=(0, 4), value=m_m3, fmt=int)
                    bitfields_1 |= (bitfields_1 & -16) | (m_m3 & 0xf)

                    dump.add_record(access="m4", bits=(4, 4), value=m_m4, fmt=int)
                    bitfields_1 |= (bitfields_1 & -241) | ((m_m4 & 0xf) << 4)

                    pieces.append(bitfields_1.to_bytes(1, "little", signed=False))
                    bitfields_1_dump.value = str(bitfields_1)
                    bitfields_1_dump.memory = pieces[-1]

                    m5_dump = dump.add_record(access="m5", fmt=uint8)
                    uint8.__pack__(m_m5, pieces, m5_dump)

                    bitfields_2_dump = dump.add_record()
                    bitfields_2 = 0

                    dump.add_record(access="m6", bits=(0, 4), value=m_m6, fmt=int)
                    bitfields_2 |= (bitfields_2 & -16) | (m_m6 & 0xf)

                    dump.add_record(access="m7", bits=(4, 8), value=m_m7, fmt=int)
                    bitfields_2 |= (bitfields_2 & -4081) | ((m_m7 & 0xff) << 4)

                    pieces.append(bitfields_2.to_bytes(2, "little", signed=False))
                    bitfields_2_dump.value = str(bitfields_2)
                    bitfields_2_dump.memory = pieces[-1]

            @classmethod
            def __unpack__(cls, buffer: bytes, offset: int, dump: Optional[Record] = None) -> Tuple["MyStruct", int]:
                structure = list.__new__(cls)

                if dump is None:
                    bitfields_0, offset = cls.m0.__unpack__(buffer, offset, dump, "little", nbytes=2, signed=False)

                    m_m0 = (bitfields_0 >> 0) & 0xf

                    m_m1 = (bitfields_0 >> 4) & 0xff

                    m_m2, offset = uint8.__unpack__(buffer, offset, dump)

                    bitfields_1, offset = cls.m3.__unpack__(buffer, offset, dump, "little", nbytes=1, signed=False)

                    m_m3 = (bitfields_1 >> 0) & 0xf

                    m_m4 = (bitfields_1 >> 4) & 0xf

                    m_m5, offset = uint8.__unpack__(buffer, offset, dump)

                    bitfields_2, offset = cls.m6.__unpack__(buffer, offset, dump, "little", nbytes=2, signed=False)

                    m_m6 = (bitfields_2 >> 0) & 0xf

                    m_m7 = (bitfields_2 >> 4) & 0xff

                else:
                    bitfields_0_dump = dump.add_record()
                    bitfields_0, offset = cls.m0.__unpack__(buffer, offset, bitfields_0_dump, "little", nbytes=2, signed=False)

                    m_m0 = (bitfields_0 >> 0) & 0xf
                    dump.add_record(access="m0", bits=(0, 4), value=m_m0, fmt=int)

                    m_m1 = (bitfields_0 >> 4) & 0xff
                    dump.add_record(access="m1", bits=(4, 8), value=m_m1, fmt=int)

                    m2_dump = dump.add_record(access="m2", fmt=uint8)
                    m_m2, offset = uint8.__unpack__(buffer, offset, m2_dump)

                    bitfields_1_dump = dump.add_record()
                    bitfields_1, offset = cls.m3.__unpack__(buffer, offset, bitfields_1_dump, "little", nbytes=1, signed=False)

                    m_m3 = (bitfields_1 >> 0) & 0xf
                    dump.add_record(access="m3", bits=(0, 4), value=m_m3, fmt=int)

                    m_m4 = (bitfields_1 >> 4) & 0xf
                    dump.add_record(access="m4", bits=(4, 4), value=m_m4, fmt=int)

                    m5_dump = dump.add_record(access="m5", fmt=uint8)
                    m_m5, offset = uint8.__unpack__(buffer, offset, m5_dump)

                    bitfields_2_dump = dump.add_record()
                    bitfields_2, offset = cls.m6.__unpack__(buffer, offset, bitfields_2_dump, "little", nbytes=2, signed=False)

                    m_m6 = (bitfields_2 >> 0) & 0xf
                    dump.add_record(access="m6", bits=(0, 4), value=m_m6, fmt=int)

                    m_m7 = (bitfields_2 >> 4) & 0xff
                    dump.add_record(access="m7", bits=(4, 8), value=m_m7, fmt=int)

                structure[:] = (m_m0, m_m1, m_m2, m_m3, m_m4, m_m5, m_m6, m_m7)

                return structure, offset

            __eq__ = list.__eq__

            __ne__ = list.__ne__

            def __repr__(self) -> str:
                try:
                    return f"{type(self).__name__}(m0={self.m0!r}, m1={self.m1!r}, m2={self.m2!r}, m3={self.m3!r}, m4={self.m4!r}, m5={self.m5!r}, m6={self.m6!r}, m7={self.m7!r})"
                except Exception:
                    return f"{type(self).__name__}()"

            """
        ),
    )


class TestArtificialSplit(Case):

    """Many bit fields get grouped separately when using nbytes."""

    class MyStruct(Structure, fieldorder="least_to_most"):
        m1: int = bitfield_member(typ=int, size=4)
        m2: int = bitfield_member(typ=int, size=2)

        m3: int = bitfield_member(typ=int, size=4, nbytes=2)
        m4: int = bitfield_member(typ=int, size=4)

    data = CaseData(
        fmt=MyStruct,
        bindata=b"\x21\x43\x00",
        nbytes=3,
        values=(MyStruct(m1=1, m2=2, m3=3, m4=4), [1, 2, 3, 4], (1, 2, 3, 4)),
        dump=Baseline(
            """
            +--------+--------+-------+-------------------+----------+
            | Offset | Access | Value | Bytes             | Format   |
            +--------+--------+-------+-------------------+----------+
            |        |        |       |                   | MyStruct |
            | 0      |        | 33    | 21                |          |
            |  [0:4] | m1     | 1     | ....0001          | int      |
            |  [4:6] | m2     | 2     | ..10....          | int      |
            | 1      |        | 67    | 43 00             |          |
            |  [0:4] | m3     | 3     | ........ ....0011 | int      |
            |  [4:8] | m4     | 4     | ........ 0100.... | int      |
            +--------+--------+-------+-------------------+----------+
            """
        ),
        excess=Baseline(
            """
            +--------+--------+----------------+-------------------+----------+
            | Offset | Access | Value          | Bytes             | Format   |
            +--------+--------+----------------+-------------------+----------+
            |        |        |                |                   | MyStruct |
            | 0      |        | 33             | 21                |          |
            |  [0:4] | m1     | 1              | ....0001          | int      |
            |  [4:6] | m2     | 2              | ..10....          | int      |
            | 1      |        | 67             | 43 00             |          |
            |  [0:4] | m3     | 3              | ........ ....0011 | int      |
            |  [4:8] | m4     | 4              | ........ 0100.... | int      |
            +--------+--------+----------------+-------------------+----------+
            | 3      |        | <excess bytes> | 99                |          |
            +--------+--------+----------------+-------------------+----------+

            ExcessMemoryError occurred during unpack operation:

            1 unconsumed bytes
            """
        ),
        shortage=Baseline(
            """
            +--------+--------+----------------------+----------+----------+
            | Offset | Access | Value                | Bytes    | Format   |
            +--------+--------+----------------------+----------+----------+
            |        |        |                      |          | MyStruct |
            | 0      |        | 33                   | 21       |          |
            |  [0:4] | m1     | 1                    | ....0001 | int      |
            |  [4:6] | m2     | 2                    | ..10.... | int      |
            | 1      |        | <insufficient bytes> | 43       |          |
            +--------+--------+----------------------+----------+----------+

            InsufficientMemoryError occurred during unpack operation:

            1 too few bytes to unpack (2 needed, only 1 available)
            """
        ),
        implementation=Baseline(
            """
            def __init__(self, *, m1: int, m2: int, m3: int, m4: int) -> None:
                if not 0 <= m1 <= 15:
                   raise ValueError("'m1' out of range, 0 <= m1 <= 15")

                if not 0 <= m2 <= 3:
                   raise ValueError("'m2' out of range, 0 <= m2 <= 3")

                if not 0 <= m3 <= 15:
                   raise ValueError("'m3' out of range, 0 <= m3 <= 15")

                if not 0 <= m4 <= 15:
                   raise ValueError("'m4' out of range, 0 <= m4 <= 15")

                self[:] = (m1, m2, m3, m4)

            @m1.getter
            def m1(self) -> int:
                return self[0]

            @m1.setter
            def m1(self, value: int) -> None:
                if not 0 <= value <= 15:
                   raise ValueError("out of range, 0 <= value <= 15")
                self[0] = value

            @m2.getter
            def m2(self) -> int:
                return self[1]

            @m2.setter
            def m2(self, value: int) -> None:
                if not 0 <= value <= 3:
                   raise ValueError("out of range, 0 <= value <= 3")
                self[1] = value

            @m3.getter
            def m3(self) -> int:
                return self[2]

            @m3.setter
            def m3(self, value: int) -> None:
                if not 0 <= value <= 15:
                   raise ValueError("out of range, 0 <= value <= 15")
                self[2] = value

            @m4.getter
            def m4(self) -> int:
                return self[3]

            @m4.setter
            def m4(self, value: int) -> None:
                if not 0 <= value <= 15:
                   raise ValueError("out of range, 0 <= value <= 15")
                self[3] = value

            @classmethod
            def __pack__(cls, value, pieces: List[bytes], dump: Optional[Record] = None) -> None:
                (m_m1, m_m2, m_m3, m_m4) = value

                if dump is None:
                    bitfields_0 = 0

                    bitfields_0 |= (bitfields_0 & -16) | (m_m1 & 0xf)

                    bitfields_0 |= (bitfields_0 & -49) | ((m_m2 & 0x3) << 4)

                    pieces.append(bitfields_0.to_bytes(1, "little", signed=False))

                    bitfields_1 = 0

                    bitfields_1 |= (bitfields_1 & -16) | (m_m3 & 0xf)

                    bitfields_1 |= (bitfields_1 & -241) | ((m_m4 & 0xf) << 4)

                    pieces.append(bitfields_1.to_bytes(2, "little", signed=False))

                else:
                    bitfields_0_dump = dump.add_record()
                    bitfields_0 = 0

                    dump.add_record(access="m1", bits=(0, 4), value=m_m1, fmt=int)
                    bitfields_0 |= (bitfields_0 & -16) | (m_m1 & 0xf)

                    dump.add_record(access="m2", bits=(4, 2), value=m_m2, fmt=int)
                    bitfields_0 |= (bitfields_0 & -49) | ((m_m2 & 0x3) << 4)

                    pieces.append(bitfields_0.to_bytes(1, "little", signed=False))
                    bitfields_0_dump.value = str(bitfields_0)
                    bitfields_0_dump.memory = pieces[-1]

                    bitfields_1_dump = dump.add_record()
                    bitfields_1 = 0

                    dump.add_record(access="m3", bits=(0, 4), value=m_m3, fmt=int)
                    bitfields_1 |= (bitfields_1 & -16) | (m_m3 & 0xf)

                    dump.add_record(access="m4", bits=(4, 4), value=m_m4, fmt=int)
                    bitfields_1 |= (bitfields_1 & -241) | ((m_m4 & 0xf) << 4)

                    pieces.append(bitfields_1.to_bytes(2, "little", signed=False))
                    bitfields_1_dump.value = str(bitfields_1)
                    bitfields_1_dump.memory = pieces[-1]

            @classmethod
            def __unpack__(cls, buffer: bytes, offset: int, dump: Optional[Record] = None) -> Tuple["MyStruct", int]:
                structure = list.__new__(cls)

                if dump is None:
                    bitfields_0, offset = cls.m1.__unpack__(buffer, offset, dump, "little", nbytes=1, signed=False)

                    m_m1 = (bitfields_0 >> 0) & 0xf

                    m_m2 = (bitfields_0 >> 4) & 0x3

                    bitfields_1, offset = cls.m3.__unpack__(buffer, offset, dump, "little", nbytes=2, signed=False)

                    m_m3 = (bitfields_1 >> 0) & 0xf

                    m_m4 = (bitfields_1 >> 4) & 0xf

                else:
                    bitfields_0_dump = dump.add_record()
                    bitfields_0, offset = cls.m1.__unpack__(buffer, offset, bitfields_0_dump, "little", nbytes=1, signed=False)

                    m_m1 = (bitfields_0 >> 0) & 0xf
                    dump.add_record(access="m1", bits=(0, 4), value=m_m1, fmt=int)

                    m_m2 = (bitfields_0 >> 4) & 0x3
                    dump.add_record(access="m2", bits=(4, 2), value=m_m2, fmt=int)

                    bitfields_1_dump = dump.add_record()
                    bitfields_1, offset = cls.m3.__unpack__(buffer, offset, bitfields_1_dump, "little", nbytes=2, signed=False)

                    m_m3 = (bitfields_1 >> 0) & 0xf
                    dump.add_record(access="m3", bits=(0, 4), value=m_m3, fmt=int)

                    m_m4 = (bitfields_1 >> 4) & 0xf
                    dump.add_record(access="m4", bits=(4, 4), value=m_m4, fmt=int)

                structure[:] = (m_m1, m_m2, m_m3, m_m4)

                return structure, offset

            __eq__ = list.__eq__

            __ne__ = list.__ne__

            def __repr__(self) -> str:
                try:
                    return f"{type(self).__name__}(m1={self.m1!r}, m2={self.m2!r}, m3={self.m3!r}, m4={self.m4!r})"
                except Exception:
                    return f"{type(self).__name__}()"

            """
        ),
    )


class TestTypDefault:

    """Test typ parameter default behavior."""

    def test_defaults_to_int(self):
        """Test defaults to int when no annotation."""

        class Struct(Structure):

            """Sample Structure."""

            m1 = bitfield_member(size=4)

        assert Struct.m1.typ is int
