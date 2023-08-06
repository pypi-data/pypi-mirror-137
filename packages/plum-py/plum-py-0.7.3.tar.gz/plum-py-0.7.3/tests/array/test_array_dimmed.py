# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# Copyright 2021 Daniel Mark Gass, see __about__.py for license information.
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
"""Test DimmedArrayX transform."""

import pytest

from baseline import Baseline

from plum.array import ArrayX
from plum.conformance import Case, CaseData, wrap_message
from plum.items import ItemsX
from plum.littleendian import uint8, uint16

varies = ItemsX("varies")

dims_array = ArrayX("dims_array", fmt=uint8, dims=[2])

single_dimmed_array = ArrayX("single_dimmed_array", fmt=uint8, dims=uint16)
multi_dimmed_array = ArrayX("multi_dimmed_array", fmt=uint8, dims=dims_array)


class TestSingle(Case):

    """Test single dim dimmed array."""

    data = CaseData(
        fmt=single_dimmed_array,
        bindata=bytes.fromhex("040001020304"),
        nbytes=None,
        values=([1, 2, 3, 4],),
        dump=Baseline(
            """
            +--------+--------+-------+-------+---------------------+
            | Offset | Access | Value | Bytes | Format              |
            +--------+--------+-------+-------+---------------------+
            |        |        |       |       | single_dimmed_array |
            | 0      | len()  | 4     | 04 00 | uint16              |
            | 2      | [0]    | 1     | 01    | uint8               |
            | 3      | [1]    | 2     | 02    | uint8               |
            | 4      | [2]    | 3     | 03    | uint8               |
            | 5      | [3]    | 4     | 04    | uint8               |
            +--------+--------+-------+-------+---------------------+
            """
        ),
        excess=Baseline(
            """
            +--------+--------+----------------+-------+---------------------+
            | Offset | Access | Value          | Bytes | Format              |
            +--------+--------+----------------+-------+---------------------+
            |        |        |                |       | single_dimmed_array |
            | 0      | len()  | 4              | 04 00 | uint16              |
            | 2      | [0]    | 1              | 01    | uint8               |
            | 3      | [1]    | 2              | 02    | uint8               |
            | 4      | [2]    | 3              | 03    | uint8               |
            | 5      | [3]    | 4              | 04    | uint8               |
            +--------+--------+----------------+-------+---------------------+
            | 6      |        | <excess bytes> | 99    |                     |
            +--------+--------+----------------+-------+---------------------+

            ExcessMemoryError occurred during unpack operation:

            1 unconsumed bytes
            """
        ),
        shortage=Baseline(
            """
            +--------+--------+----------------------+-------+---------------------+
            | Offset | Access | Value                | Bytes | Format              |
            +--------+--------+----------------------+-------+---------------------+
            |        |        |                      |       | single_dimmed_array |
            | 0      | len()  | 4                    | 04 00 | uint16              |
            | 2      | [0]    | 1                    | 01    | uint8               |
            | 3      | [1]    | 2                    | 02    | uint8               |
            | 4      | [2]    | 3                    | 03    | uint8               |
            |        | [3]    | <insufficient bytes> |       | uint8               |
            +--------+--------+----------------------+-------+---------------------+

            InsufficientMemoryError occurred during unpack operation:

            1 too few bytes to unpack 'uint8' (1 needed, only 0 available)
            """
        ),
    )


class TestMulti(Case):

    """Test multiple dims dimmed array."""

    data = CaseData(
        fmt=multi_dimmed_array,
        bindata=bytes.fromhex("020201020304"),
        nbytes=None,
        values=([[1, 2], [3, 4]],),
        dump=Baseline(
            """
            +--------+----------+-------+-------+--------------------+
            | Offset | Access   | Value | Bytes | Format             |
            +--------+----------+-------+-------+--------------------+
            |        |          |       |       | multi_dimmed_array |
            |        | --dims-- |       |       | dims_array         |
            | 0      |   [0]    | 2     | 02    | uint8              |
            | 1      |   [1]    | 2     | 02    | uint8              |
            |        | [0]      |       |       |                    |
            | 2      |   [0]    | 1     | 01    | uint8              |
            | 3      |   [1]    | 2     | 02    | uint8              |
            |        | [1]      |       |       |                    |
            | 4      |   [0]    | 3     | 03    | uint8              |
            | 5      |   [1]    | 4     | 04    | uint8              |
            +--------+----------+-------+-------+--------------------+
            """
        ),
        excess=Baseline(
            """
            +--------+----------+----------------+-------+--------------------+
            | Offset | Access   | Value          | Bytes | Format             |
            +--------+----------+----------------+-------+--------------------+
            |        |          |                |       | multi_dimmed_array |
            |        | --dims-- |                |       | dims_array         |
            | 0      |   [0]    | 2              | 02    | uint8              |
            | 1      |   [1]    | 2              | 02    | uint8              |
            |        | [0]      |                |       |                    |
            | 2      |   [0]    | 1              | 01    | uint8              |
            | 3      |   [1]    | 2              | 02    | uint8              |
            |        | [1]      |                |       |                    |
            | 4      |   [0]    | 3              | 03    | uint8              |
            | 5      |   [1]    | 4              | 04    | uint8              |
            +--------+----------+----------------+-------+--------------------+
            | 6      |          | <excess bytes> | 99    |                    |
            +--------+----------+----------------+-------+--------------------+

            ExcessMemoryError occurred during unpack operation:

            1 unconsumed bytes
            """
        ),
        shortage=Baseline(
            """
            +--------+----------+----------------------+-------+--------------------+
            | Offset | Access   | Value                | Bytes | Format             |
            +--------+----------+----------------------+-------+--------------------+
            |        |          |                      |       | multi_dimmed_array |
            |        | --dims-- |                      |       | dims_array         |
            | 0      |   [0]    | 2                    | 02    | uint8              |
            | 1      |   [1]    | 2                    | 02    | uint8              |
            |        | [0]      |                      |       |                    |
            | 2      |   [0]    | 1                    | 01    | uint8              |
            | 3      |   [1]    | 2                    | 02    | uint8              |
            |        | [1]      |                      |       |                    |
            | 4      |   [0]    | 3                    | 03    | uint8              |
            |        |   [1]    | <insufficient bytes> |       | uint8              |
            +--------+----------+----------------------+-------+--------------------+

            InsufficientMemoryError occurred during unpack operation:

            1 too few bytes to unpack 'uint8' (1 needed, only 0 available)
            """
        ),
    )


class TestProperties:

    """Test transform properties."""

    def test_all(self):
        assert single_dimmed_array.name == "single_dimmed_array"
        assert single_dimmed_array.fmt is uint8
        assert single_dimmed_array.dims is uint16


class TestExceptions:

    """Test invalid dims_fmt values."""

    expected_array_message = Baseline(
        """
        invalid ArrayX 'dims', must be single dim and non-greedy
        """
    )

    def test_greedy(self):
        with pytest.raises(TypeError) as trap:
            ArrayX("da", fmt=uint8, dims=ArrayX("a", fmt=uint8))

        assert wrap_message(trap.value) == self.expected_array_message

    def test_not_single_dim(self):
        with pytest.raises(TypeError) as trap:
            ArrayX("da", fmt=uint8, dims=ArrayX("a", fmt=uint8, dims=[2, 2]))

        assert wrap_message(trap.value) == self.expected_array_message

    def test_bad_transform(self):
        expected_message = Baseline(
            """
            'ItemsX' object is not iterable
            """
        )

        with pytest.raises(TypeError) as trap:
            ArrayX("da", fmt=uint8, dims=varies)

        assert wrap_message(trap.value) == expected_message
