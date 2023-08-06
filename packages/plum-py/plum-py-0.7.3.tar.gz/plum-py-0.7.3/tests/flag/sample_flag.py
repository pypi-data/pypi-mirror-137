# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# Copyright 2021 Daniel Mark Gass, see __about__.py for license information.
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
"""Sample integer flag enumeration"""

from enum import IntFlag


class Register(IntFlag):

    """Sample integer flag enumeration."""

    SP = 1
    R0 = 2
    R1 = 4
