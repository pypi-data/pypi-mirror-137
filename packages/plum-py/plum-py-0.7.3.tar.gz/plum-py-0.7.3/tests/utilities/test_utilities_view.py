# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# Copyright 2021 Daniel Mark Gass, see __about__.py for license information.
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
"""Verify view() base method functionality."""

import pytest
from baseline import Baseline

from plum.conformance import wrap_message
from plum.none import NoneX

nil = NoneX("nil")


class TestExceptions:

    """Test view() exceptions."""

    def test_unsupported_plumtype(self):
        """Verify creating a view with an unsupported type raises an exception."""
        with pytest.raises(TypeError) as trap:
            nil.view(buffer=bytearray())

        expected = Baseline("""'nil' does not support view()""")

        assert wrap_message(trap.value) == expected
