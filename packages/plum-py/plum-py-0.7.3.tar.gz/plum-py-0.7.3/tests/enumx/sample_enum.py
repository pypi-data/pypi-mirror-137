# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# Copyright 2021 Daniel Mark Gass, see __about__.py for license information.
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
"""Sample integer enumeration"""

from enum import IntEnum


class Register(IntEnum):

    """Tested class."""

    PC = 0
    SP = 1
    R0 = 2
    R1 = 3
