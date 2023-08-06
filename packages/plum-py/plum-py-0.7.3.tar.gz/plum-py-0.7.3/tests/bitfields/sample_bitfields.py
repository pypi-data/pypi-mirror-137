# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# Copyright 2021 Daniel Mark Gass, see __about__.py for license information.
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
"""Sample BitFields data store class."""

from enum import IntEnum

from plum.bitfields import bitfield, BitFields


class Register(IntEnum):

    """Tested class."""

    PC = 0
    SP = 1
    R0 = 2
    R1 = 3


class MyBits(BitFields, nbytes=2, default=0x0):

    """Sample BitFields subclass."""

    f1: int = bitfield(lsb=0, size=8, default=0xAB)
    f2: Register = bitfield(lsb=8, size=4, typ=Register)
    f3: bool = bitfield(lsb=12, size=1, typ=bool)
    f4: bool = bitfield(lsb=13, size=1, typ=bool)
