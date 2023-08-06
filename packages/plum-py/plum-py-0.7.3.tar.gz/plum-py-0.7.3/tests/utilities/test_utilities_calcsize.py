# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# Copyright 2021 Daniel Mark Gass, see __about__.py for license information.
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
"""Test calcsize() utility function."""

import pytest
from baseline import Baseline

from plum.array import ArrayX
from plum.exceptions import SizeError
from plum.littleendian import uint8, uint16
from plum.structure import Structure, member
from plum.utilities import calcsize

greedy_array = ArrayX("greedy_array", fmt=uint8)


class TestFixed:
    class Struct(Structure):
        m0 = member(fmt=uint8)

    def test_transform(self):
        assert calcsize(uint8) == 1

    def test_data_store_type(self):
        assert calcsize(self.Struct) == 1

    def test_data_store_instance(self):
        assert calcsize(self.Struct(m0=0)) == 1

    def test_dict(self):
        assert calcsize({"a": uint8, "b": uint16}) == 3

    def test_list(self):
        assert calcsize([uint8, uint16]) == 3

    def test_tuple(self):
        assert calcsize((uint8, uint16)) == 3


class TestVariable:
    class Struct(Structure):
        m0 = member(fmt=greedy_array)

    expected_message = Baseline(
        """
        size varies
        """
    )

    def test_transform(self):
        expected_message = Baseline(
            """
            'greedy_array' transform sizes vary
            """
        )
        with pytest.raises(SizeError) as trap:
            calcsize(greedy_array)
        assert str(trap.value) == expected_message

    def test_data_store_type(self):
        expected_message = Baseline(
            """
            size varies
            """
        )
        with pytest.raises(SizeError) as trap:
            calcsize(calcsize(self.Struct))
        assert str(trap.value) == expected_message

    def test_dict(self):
        with pytest.raises(SizeError) as trap:
            calcsize({"a": uint8, "b": None})
        assert str(trap.value) == self.expected_message

    def test_list(self):
        with pytest.raises(SizeError) as trap:
            calcsize([uint8, None])
        assert str(trap.value) == self.expected_message

    def test_tuple(self):
        with pytest.raises(SizeError) as trap:
            calcsize((uint8, None))
        assert str(trap.value) == self.expected_message

    def test_none(self):
        with pytest.raises(SizeError) as trap:
            calcsize(None)
        assert str(trap.value) == self.expected_message


class TestInvalid:
    def test_invalid(self):
        expected_message = Baseline(
            """
            invalid format <class 'int'>
            """
        )

        with pytest.raises(TypeError) as trap:
            calcsize(int)

        assert str(trap.value) == expected_message
