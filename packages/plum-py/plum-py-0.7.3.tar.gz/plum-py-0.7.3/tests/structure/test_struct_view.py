# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# Copyright 2021 Daniel Mark Gass, see __about__.py for license information.
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
"""Test operations for structure view to bytes buffer."""

from collections.abc import Sequence

import pytest
from baseline import Baseline

from plum.conformance import wrap_message
from plum.array import ArrayX
from plum.int import IntView
from plum.littleendian import uint8, uint16
from plum.structure import Structure, member
from plum.structure._structureview import StructureView
from plum.utilities import pack


class FourElementStruct(Structure):

    """Sample structure with four members."""

    m1: int = member(fmt=uint8)
    m2: int = member(fmt=uint8)
    m3: int = member(fmt=uint8)
    m4: int = member(fmt=uint8)


class MyStruct(Structure):

    """Sample structure with two members."""

    m1: int = member(fmt=uint8)
    m2: int = member(fmt=uint16)


class StructWithIgnore(Structure):

    """Sample structure with member that is ignored."""

    not_ignored: int = member(fmt=uint8, default=1)
    ignored: int = member(fmt=uint8, default=0, ignore=True)


class VariableSizeStruct(Structure):

    """Sample variably sized Structure."""

    m1: list = member(fmt=ArrayX("array", fmt=uint8))


class TestExceptions:

    """Test exception corner cases."""

    def test_variable_sized(self):
        """Test view of structure with variable size not allowed."""
        with pytest.raises(TypeError) as trap:
            VariableSizeStruct.view(bytearray(5), offset=1)

        expected = Baseline(
            """
            cannot create view for structure 'VariableSizeStruct' with variable
            size
            """
        )

        assert wrap_message(trap.value) == expected


class TestStructureView:

    """Test operations for structure view to bytes buffer."""

    def test_attribute_access(self):
        """Test accessing members with attribute syntax."""
        memory_backing = bytearray([0xFF, 0x02, 0x05, 0x00, 0xFF])
        struct_view = MyStruct.view(memory_backing, offset=1)

        assert struct_view.m1 == 2
        assert struct_view.m2 == 5

        assert isinstance(struct_view.m1, IntView)
        assert isinstance(struct_view.m2, IntView)

        struct_view.m1 = 1
        assert isinstance(struct_view.m1, IntView)  # verify view not overwritten
        assert struct_view == MyStruct(m1=1, m2=5)
        assert memory_backing == bytearray(b"\xff\x01\x05\x00\xff")

        struct_view.m2 = 3
        assert isinstance(struct_view.m2, IntView)  # verify view not overwritten
        assert struct_view == MyStruct(m1=1, m2=3)
        assert memory_backing == bytearray(b"\xff\x01\x03\x00\xff")

    def test_item_access(self):
        """Test accessing members with item/index syntax."""
        memory_backing = bytearray([0x03, 0x02, 0x01, 0xFF])
        struct_view = MyStruct.view(memory_backing, offset=0)

        assert struct_view[0] == 3
        assert struct_view[1] == 258

        assert isinstance(struct_view[0], IntView)
        assert isinstance(struct_view[1], IntView)

        struct_view[0] = 15
        assert isinstance(struct_view[0], IntView)  # verify view not overwritten
        assert struct_view == MyStruct(m1=15, m2=258)
        assert memory_backing == bytearray(b"\x0f\x02\x01\xff")

        struct_view[1] = 0
        assert isinstance(struct_view[1], IntView)  # verify view not overwritten
        assert struct_view == MyStruct(m1=15, m2=0)
        assert memory_backing == bytearray(b"\x0f\x00\x00\xff")

    def test_representations(self):
        """Test repr and dump representations."""
        memory_backing = bytearray([0xFF, 0x01, 0x02, 0x00, 0xFF])
        struct_view = MyStruct.view(memory_backing, offset=1)
        expected = Baseline(
            """
        +--------+--------+-------+-------+----------+
        | Offset | Access | Value | Bytes | Format   |
        +--------+--------+-------+-------+----------+
        |        |        |       |       | MyStruct |
        | 1      | m1     | 1     | 01    | uint8    |
        | 2      | m2     | 2     | 02 00 | uint16   |
        +--------+--------+-------+-------+----------+
        """
        )

        assert repr(struct_view) == "<view at 0x1: MyStruct(m1=1, m2=2)>"
        assert struct_view.asdict() == {"m1": 1, "m2": 2}
        assert str(struct_view.dump) == expected

    def test_comparison_behavior(self):
        """Test comparison behavior."""
        # pylint: disable=unneeded-not
        memory_backing = bytearray([0xFF, 0x01, 0x02, 0x00, 0xFF])
        my_struct_view = MyStruct.view(memory_backing, offset=1)
        struct_with_ignore_view = StructWithIgnore.view(memory_backing, offset=1)

        assert my_struct_view == [0x01, 0x02]  # list compare format
        assert my_struct_view.copy() == [1, 2]  # list from copy method
        assert struct_with_ignore_view == StructWithIgnore(
            not_ignored=1
        )  # missing member with ignore
        assert (
            struct_with_ignore_view == StructWithIgnore()
        )  # missing member with defaulting

        assert my_struct_view >= [1, 2]
        assert my_struct_view >= [1, 1]
        assert my_struct_view > [1, 1]
        assert not my_struct_view > [2, 2]

        assert my_struct_view <= [1, 2]
        assert my_struct_view <= [2, 2]
        assert my_struct_view < [2, 2]
        assert not my_struct_view < [0, 0]

        assert len(my_struct_view) == 2

    def test_arithmetic_behavior(self):
        """Test arithmetic behavior."""
        memory_backing = bytearray([0xFF, 0x01, 0x02, 0x00, 0xFF])
        my_struct_view = MyStruct.view(memory_backing, offset=1)

        assert my_struct_view + [3, 4] == [1, 2, 3, 4]
        assert [0] + my_struct_view == [0, 1, 2]

        assert my_struct_view * 2 == [1, 2, 1, 2]
        assert 3 * my_struct_view == [1, 2, 1, 2, 1, 2]

    def test_sort_behavior(self):
        """Test sort method behavior."""
        buffer = bytearray([0xFF, 0x0A, 0x0C, 0x03, 0x06, 0xFF])
        struct_view = FourElementStruct.view(buffer, offset=1)

        struct_view.sort()

        assert struct_view == [3, 6, 10, 12]
        assert struct_view.index(3) == 0
        assert struct_view.index(6) == 1
        assert struct_view.index(10) == 2
        assert struct_view.index(12) == 3
        assert buffer == bytearray(b"\xff\x03\x06\x0a\x0c\xff")

    def test_count_behavior(self):
        """Test count method behavior."""
        buffer = bytearray([0xFF, 0x01, 0x01, 0x02, 0x01, 0xFF])
        struct_view = FourElementStruct.view(buffer, offset=1)

        assert struct_view.count(1) == 3
        assert struct_view.count(2) == 1
        assert struct_view.count(3) == 0

    def test_inheritance_behavior(self):
        """Verify ``isinstance`` behavior."""
        struct_view = MyStruct.view(bytearray([0x00, 0x00, 0x00, 0x00]))

        assert isinstance(struct_view, StructureView)
        assert isinstance(struct_view, Sequence)

    def test_pack_pos_argument(self):
        """Test pack() utility supports view as positional argument."""
        buffer = bytearray(5)
        msv = MyStruct.view(buffer, offset=1)
        msv.m1 = 1
        msv.m2 = 2
        assert pack(msv, MyStruct) == bytearray([0x01, 0x02, 0x00])

    def test_pack_kw_argument(self):
        """Test pack() utility supports view as keyword argument."""
        buffer = bytearray(5)
        msv = MyStruct.view(buffer, offset=1)
        msv.m1 = 1
        msv.m2 = 2
        assert pack({"x": msv}, {"x": MyStruct}) == bytearray([0x01, 0x02, 0x00])

    def test_get(self):
        """Test get() returns unpacked value."""
        buffer = bytearray([0x00, 0x01, 0x02, 0x00, 0xFF])
        msv = MyStruct.view(buffer, offset=1)
        value = msv.unpack()
        assert isinstance(value, MyStruct)
        assert value == [1, 2]
        # changing buffer does not effect previously returned value
        buffer[0:5] = [0] * 5
        assert value == [1, 2]

    def test_set(self):
        """Test set()."""
        buffer = bytearray(5)
        msv = MyStruct.view(buffer, offset=1)
        assert msv == [0, 0]
        msv.set([1, 2])
        assert msv == [1, 2]
        assert buffer == bytearray([0x00, 0x01, 0x02, 0x00, 0x00])

    def test_setattr(self):
        """Test __setattr__() method."""
        view = MyStruct.view(bytearray(5))
        view.abc = 1
        assert view.abc == 1


class TestBlockedMethods:

    """Test structure mutation methods are blocked."""

    def test_append(self):
        """Test append() method blocked."""
        view = MyStruct.view(bytearray(5))

        with pytest.raises(TypeError) as trap:
            view.append(0)

        expected = Baseline(
            """
            'StructureView' does not support append()
            """
        )

        assert wrap_message(trap.value) == expected

    def test_clear(self):
        """Test clear() method blocked."""
        view = MyStruct.view(bytearray(5))

        with pytest.raises(TypeError) as trap:
            view.clear()

        expected = Baseline(
            """
            'StructureView' does not support clear()
            """
        )

        assert wrap_message(trap.value) == expected

    def test_delattr(self):
        """Test __delattr__() method blocked."""
        view = MyStruct.view(bytearray(5))

        with pytest.raises(TypeError) as trap:
            del view.abc

        expected = Baseline(
            """
            'StructureView' does not support attribute deletion
            """
        )

        assert wrap_message(trap.value) == expected

    def test_delitem(self):
        """Test __delitem__() method blocked."""
        view = MyStruct.view(bytearray(5))
        with pytest.raises(TypeError) as trap:
            del view[0]

        expected = Baseline(
            """
            'StructureView' does not support item deletion
            """
        )

        assert wrap_message(trap.value) == expected

    def test_extend(self):
        """Test extend() method blocked."""
        view = MyStruct.view(bytearray(5))

        with pytest.raises(TypeError) as trap:
            view.extend([0])

        expected = Baseline(
            """
            'StructureView' does not support extend()
            """
        )

        assert wrap_message(trap.value) == expected

    def test_getattr(self):
        """Test __getattr__() method only allows access to structure members."""
        view = MyStruct.view(bytearray(5))

        with pytest.raises(AttributeError) as trap:
            view.abc  # pylint: disable=pointless-statement

        expected = Baseline(
            """
            'StructureView' object has no attribute 'abc'
            """
        )

        assert wrap_message(trap.value) == expected

    def test_iadd(self):
        """Test __iadd__() method blocked."""
        view = MyStruct.view(bytearray(5))

        with pytest.raises(TypeError) as trap:
            view += [0]

        expected = Baseline(
            """
            'StructureView' does not support in-place addition
            """
        )

        assert wrap_message(trap.value) == expected

    def test_imul(self):
        """Test __imul__() method blocked."""
        view = MyStruct.view(bytearray(5))

        with pytest.raises(TypeError) as trap:
            view *= [0]

        expected = Baseline(
            """
            'StructureView' does not support in-place multiplication
            """
        )

        assert wrap_message(trap.value) == expected

    def test_insert(self):
        """Test insert() method blocked."""
        view = MyStruct.view(bytearray(5))

        with pytest.raises(TypeError) as trap:
            view.insert(0, 0)

        expected = Baseline(
            """
            'StructureView' does not support insert()
            """
        )

        assert wrap_message(trap.value) == expected

    def test_pop(self):
        """Test pop() method blocked."""
        view = MyStruct.view(bytearray(5))

        with pytest.raises(TypeError) as trap:
            view.pop(0)

        expected = Baseline(
            """
            'StructureView' does not support pop()
            """
        )

        assert wrap_message(trap.value) == expected

    def test_remove(self):
        """Test remove() method blocked."""
        view = MyStruct.view(bytearray(5))

        with pytest.raises(TypeError) as trap:
            view.remove(0)

        expected = Baseline(
            """
            'StructureView' does not support remove()
            """
        )

        assert wrap_message(trap.value) == expected

    def test_reverse(self):
        """Test reverse() method blocked."""
        view = MyStruct.view(bytearray(5))

        with pytest.raises(TypeError) as trap:
            view.reverse()

        expected = Baseline(
            """
            'StructureView' does not support reverse()
            """
        )

        assert wrap_message(trap.value) == expected
