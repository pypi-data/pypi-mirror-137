# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# Copyright 2022 Daniel Mark Gass, see __about__.py for license information.
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
"""Common typing hints."""

import sys

if sys.version_info < (3, 8):
    ByteOrderHint = str
else:
    from typing import Literal, Union

    ByteOrderHint = Union[Literal["little"], Literal["big"]]
