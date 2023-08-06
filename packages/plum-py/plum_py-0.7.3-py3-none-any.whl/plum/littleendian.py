# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# Copyright 2021 Daniel Mark Gass, see __about__.py for license information.
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
"""Common transforms in little endian format."""

from .float import FloatX
from .int import IntX


sint8 = IntX("sint8", nbytes=1, byteorder="little", signed=True)
sint16 = IntX("sint16", nbytes=2, byteorder="little", signed=True)
sint32 = IntX("sint32", nbytes=4, byteorder="little", signed=True)
sint64 = IntX("sint64", nbytes=8, byteorder="little", signed=True)

uint8 = IntX("uint8", nbytes=1, byteorder="little", signed=False)
uint16 = IntX("uint16", nbytes=2, byteorder="little", signed=False)
uint32 = IntX("uint32", nbytes=4, byteorder="little", signed=False)
uint64 = IntX("uint64", nbytes=8, byteorder="little", signed=False)

single = FloatX("single", nbytes=4, byteorder="little")
double = FloatX("double", nbytes=8, byteorder="little")
