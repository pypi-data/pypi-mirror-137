# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# Copyright 2021 Daniel Mark Gass, see __about__.py for license information.
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
"""Test pointer views."""

from plum.int import IntX
from plum.littleendian import uint16


pointeruint16 = IntX("pointeruint16", nbytes=1, dref=uint16)
pointeruint16pointer = IntX("pointeruint16pointer", nbytes=1, dref=pointeruint16)


class TestBasics:

    """Test basic features of pointer views."""

    def test_int_behavior(self):
        """Test that it behaves as an integer."""
        buffer = bytearray([0, 4, 0, 0, 1, 2, 3, 4])
        pointer = pointeruint16.view(buffer, 1)
        assert pointer == 4

        pointer.set(2)
        assert buffer == bytearray([0, 2, 0, 0, 1, 2, 3, 4])

    def test_dref_read(self):
        """Test dereferencing produces correct value."""
        buffer = bytearray([0, 4, 0, 0, 1, 2, 3, 4])
        pointer = pointeruint16.view(buffer, 1)
        assert pointer[0] == 0x201
        assert pointer[1] == 0x403

        # change data behind the scenes (last byte)
        buffer[7] = 0x99
        assert pointer[1] == 0x9903

        # change pointer behind the scenes
        buffer[1] = 3
        assert pointer[0] == 0x100
        assert pointer[1] == 0x302

    def test_dref_write(self):
        """Test dereferencing with assignment writes bytes correctly."""
        buffer = bytearray([0, 4, 0, 0, 0, 0, 0, 0])
        pointer = pointeruint16.view(buffer, 1)

        pointer[0] = 0x201
        assert buffer == bytearray([0, 4, 0, 0, 1, 2, 0, 0])

        pointer[1] = 0x403
        assert buffer == bytearray([0, 4, 0, 0, 1, 2, 3, 4])

    def test_nesting(self):
        """Test nested pointers."""
        buffer = bytearray([0, 4, 0, 0, 6, 8, 1, 2, 3, 4])
        pointer = pointeruint16pointer.view(buffer, 1)

        assert pointer == 4
        assert pointer[0] == 6
        assert pointer[0][0] == 0x201
        assert pointer[0][1] == 0x403
        assert pointer[1][0] == 0x403
