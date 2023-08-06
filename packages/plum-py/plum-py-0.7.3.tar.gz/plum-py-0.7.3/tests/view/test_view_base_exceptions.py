# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# Copyright 2021 Daniel Mark Gass, see __about__.py for license information.
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
"""Test base view type exceptions."""

import pytest

from baseline import Baseline

from plum.bigendian import uint16
from plum.conformance import wrap_message
from plum.exceptions import UnpackError
from plum.view import PlumView


class TestExceptions:

    """Test base view type exceptions."""

    def test_init_bad_plumtype(self):
        """Verify initializing without a valid plum type raises an exception."""
        with pytest.raises(TypeError) as trap:
            PlumView(fmt=0, buffer=bytearray(), offset=0)

        expected = Baseline("""invalid plumtype""")

        assert wrap_message(trap.value) == expected

    def test_pack_issues(self):
        """Verify initializing without a valid plum type raises an exception."""
        expected = Baseline(
            """
            +--------+----------------------+-------+--------+
            | Offset | Value                | Bytes | Format |
            +--------+----------------------+-------+--------+
            | 0      | <insufficient bytes> | 00    | uint16 |
            +--------+----------------------+-------+--------+

            InsufficientMemoryError occurred during unpack operation:

            1 too few bytes to unpack 'uint16' (2 needed, only 1 available)
            """
        )

        view = uint16.view(b"\x00")

        with pytest.raises(UnpackError) as trap:
            view.pack()

        assert wrap_message(trap.value) == expected

    def test_hash(self):
        expected = Baseline(
            """
            unhashable type: IntView
            """
        )

        view = uint16.view(b"\x00\x00")

        with pytest.raises(TypeError) as trap:
            hash(view)

        assert wrap_message(trap.value) == expected
