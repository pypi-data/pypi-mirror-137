# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# Copyright 2021 Daniel Mark Gass, see __about__.py for license information.
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
"""Test use of BitFields as a typ in bitfield_member()."""

# pylint: disable=too-many-lines

from baseline import Baseline

from plum.bigendian import uint8
from plum.bitfields import BitFields, bitfield
from plum.conformance import Case, CaseData
from plum.structure import Structure, member, bitfield_member


class Bits(BitFields, nbytes=1):

    b1: int = bitfield(size=1, typ=bool)
    b2: int = bitfield(size=1, typ=bool)


class Test(Case):

    """bitfield_member(typ=BitFields)."""

    class MyStruct(Structure):

        m1: Bits = bitfield_member(typ=Bits, size=2)
        m2: int = bitfield_member(typ=int, size=6)
        m3: int = member(fmt=uint8, default=0xFF)

    data = CaseData(
        fmt=MyStruct,
        bindata=b"\x80\xff",
        nbytes=2,
        values=(
            MyStruct(m1=Bits.from_int(2), m2=0, m3=0xFF),
            [2, 0, 0xFF],
        ),
        dump=Baseline(
            """
            +--------+--------+-------+----------+----------+
            | Offset | Access | Value | Bytes    | Format   |
            +--------+--------+-------+----------+----------+
            |        |        |       |          | MyStruct |
            | 0      |        | 128   | 80       |          |
            |        | m1     | 2     |          | Bits     |
            |  [7]   |   b1   | True  | 1....... | bool     |
            |  [6]   |   b2   | False | .0...... | bool     |
            |  [0:6] | m2     | 0     | ..000000 | int      |
            | 1      | m3     | 255   | ff       | uint8    |
            +--------+--------+-------+----------+----------+
            """
        ),
        excess=Baseline(
            """
            +--------+--------+----------------+----------+----------+
            | Offset | Access | Value          | Bytes    | Format   |
            +--------+--------+----------------+----------+----------+
            |        |        |                |          | MyStruct |
            | 0      |        | 128            | 80       |          |
            |        | m1     | 2              |          | Bits     |
            |  [7]   |   b1   | True           | 1....... | bool     |
            |  [6]   |   b2   | False          | .0...... | bool     |
            |  [0:6] | m2     | 0              | ..000000 | int      |
            | 1      | m3     | 255            | ff       | uint8    |
            +--------+--------+----------------+----------+----------+
            | 2      |        | <excess bytes> | 99       |          |
            +--------+--------+----------------+----------+----------+

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
            | 0      |        | 128                  | 80       |          |
            |        | m1     | 2                    |          | Bits     |
            |  [7]   |   b1   | True                 | 1....... | bool     |
            |  [6]   |   b2   | False                | .0...... | bool     |
            |  [0:6] | m2     | 0                    | ..000000 | int      |
            |        | m3     | <insufficient bytes> |          | uint8    |
            +--------+--------+----------------------+----------+----------+

            InsufficientMemoryError occurred during unpack operation:

            1 too few bytes to unpack 'uint8' (1 needed, only 0 available)
            """
        ),
        implementation=Baseline(
            """
            def __init__(self, *, m1: Bits, m2: int, m3: int = 255) -> None:
                if not 0 <= m1 <= 3:
                   raise ValueError("'m1' out of range, 0 <= m1 <= 3")

                if not 0 <= m2 <= 63:
                   raise ValueError("'m2' out of range, 0 <= m2 <= 63")

                self[:] = (m1, m2, m3)

            @m1.getter
            def m1(self) -> Bits:
                return self[0]

            @m1.setter
            def m1(self, value: Bits) -> None:
                if not 0 <= value <= 3:
                   raise ValueError("out of range, 0 <= value <= 3")
                self[0] = Bits(value)

            @m2.getter
            def m2(self) -> int:
                return self[1]

            @m2.setter
            def m2(self, value: int) -> None:
                if not 0 <= value <= 63:
                   raise ValueError("out of range, 0 <= value <= 63")
                self[1] = value

            @m3.getter
            def m3(self) -> int:
                return self[2]

            @m3.setter
            def m3(self, value: int) -> None:
                self[2] = value

            @classmethod
            def __pack__(cls, value, pieces: List[bytes], dump: Optional[Record] = None) -> None:
                (m_m1, m_m2, m_m3) = value

                if dump is None:
                    bitfields_0 = 0

                    bitfields_0 |= (bitfields_0 & -193) | ((m_m1 & 0x3) << 6)

                    bitfields_0 |= (bitfields_0 & -64) | (m_m2 & 0x3f)

                    pieces.append(bitfields_0.to_bytes(1, "little", signed=False))

                    uint8.__pack__(m_m3, pieces, dump)

                else:
                    bitfields_0_dump = dump.add_record()
                    bitfields_0 = 0

                    dump_m_m1 = dump.add_record(access="m1", value=int(m_m1), fmt=Bits)
                    Bits.__add_bitfields_to_dump__(m_m1, dump_m_m1, bitoffset=6)
                    bitfields_0 |= (bitfields_0 & -193) | ((m_m1 & 0x3) << 6)

                    dump.add_record(access="m2", bits=(0, 6), value=m_m2, fmt=int)
                    bitfields_0 |= (bitfields_0 & -64) | (m_m2 & 0x3f)

                    pieces.append(bitfields_0.to_bytes(1, "little", signed=False))
                    bitfields_0_dump.value = str(bitfields_0)
                    bitfields_0_dump.memory = pieces[-1]

                    m3_dump = dump.add_record(access="m3", fmt=uint8)
                    uint8.__pack__(m_m3, pieces, m3_dump)

            @classmethod
            def __unpack__(cls, buffer: bytes, offset: int, dump: Optional[Record] = None) -> Tuple["MyStruct", int]:
                structure = list.__new__(cls)

                if dump is None:
                    bitfields_0, offset = cls.m1.__unpack__(buffer, offset, dump, "little", nbytes=1, signed=False)

                    m_m1 = (bitfields_0 >> 6) & 0x3
                    m_m1 = Bits.from_int(m_m1)

                    m_m2 = (bitfields_0 >> 0) & 0x3f

                    m_m3, offset = uint8.__unpack__(buffer, offset, dump)

                else:
                    bitfields_0_dump = dump.add_record()
                    bitfields_0, offset = cls.m1.__unpack__(buffer, offset, bitfields_0_dump, "little", nbytes=1, signed=False)

                    m_m1 = (bitfields_0 >> 6) & 0x3
                    m_m1 = Bits.from_int(m_m1)
                    dump_m_m1 = dump.add_record(access="m1", value=int(m_m1), fmt=Bits)
                    Bits.__add_bitfields_to_dump__(m_m1, dump_m_m1, bitoffset=6)

                    m_m2 = (bitfields_0 >> 0) & 0x3f
                    dump.add_record(access="m2", bits=(0, 6), value=m_m2, fmt=int)

                    m3_dump = dump.add_record(access="m3", fmt=uint8)
                    m_m3, offset = uint8.__unpack__(buffer, offset, m3_dump)

                structure[:] = (m_m1, m_m2, m_m3)

                return structure, offset

            __eq__ = list.__eq__

            __ne__ = list.__ne__

            def __repr__(self) -> str:
                try:
                    return f"{type(self).__name__}(m1={self.m1!r}, m2={self.m2!r}, m3={self.m3!r})"
                except Exception:
                    return f"{type(self).__name__}()"

            """
        ),
    )
