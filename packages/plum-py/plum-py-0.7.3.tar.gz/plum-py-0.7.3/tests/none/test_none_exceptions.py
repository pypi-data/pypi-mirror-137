# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# Copyright 2021 Daniel Mark Gass, see __about__.py for license information.
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
"""Test NoneX transform exceptions."""

import pytest
from baseline import Baseline

from plum.conformance import wrap_message
from plum.exceptions import PackError
from plum.none import NoneX

nonex = NoneX("nonex")


class TestInvalidPackValue:

    expected_message = Baseline(
        """
        +--------+-------+-------+--------+
        | Offset | Value | Bytes | Format |
        +--------+-------+-------+--------+
        |        | 0     |       | nonex  |
        +--------+-------+-------+--------+

        TypeError occurred during pack operation:

        value must be 'None'
        """
    )

    def test_pack(self):
        with pytest.raises(PackError) as trap:
            nonex.pack(0)

        assert wrap_message(trap.value) == self.expected_message
        assert isinstance(trap.value.__context__, TypeError)

    def test_nbytes(self):
        with pytest.raises(PackError) as trap:
            nonex.pack_and_dump(0)

        assert wrap_message(trap.value) == self.expected_message
        assert isinstance(trap.value.__context__, TypeError)
