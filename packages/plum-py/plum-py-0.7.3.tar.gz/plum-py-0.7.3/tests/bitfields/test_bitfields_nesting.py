# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# Copyright 2021 Daniel Mark Gass, see __about__.py for license information.
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
"""Test arbitrary nesting of bit field types."""

# pylint: disable=unexpected-keyword-arg

from baseline import Baseline

from plum.bitfields import BitFields, bitfield


class Inner(BitFields, nested=True, default=0x4):

    """Sample datatype for innermost part of structure."""

    il0: int = bitfield(lsb=0, size=1, ignore=True)
    il1: int = bitfield(lsb=1, size=1, default=1)
    # empty bitfield(lsb=2, size=1)
    il2: int = bitfield(lsb=3, size=2)


class Middle(BitFields, nested=True, default=0xC, ignore=0x4):

    """Sample datatype for middle part of structure."""

    ml0: int = bitfield(lsb=0, size=1, ignore=True)
    ml1: int = bitfield(lsb=1, size=1, default=1)
    # empty bitfield(lsb=2, size=2)
    ml2: Inner = bitfield(lsb=4, size=5, typ=Inner)


class Outer(BitFields, nbytes=2, default=0x70, ignore=0x10):

    """Sample datatype for outermost part of structure."""

    ol0: int = bitfield(lsb=0, size=2, ignore=True)
    ol1: int = bitfield(lsb=2, size=2, default=1)
    # empty bitfield(lsb=4, size=3)
    ol2: Middle = bitfield(lsb=7, size=9, typ=Middle)


class TestNested:

    """Verify bit fields may be nested within bitfields arbitrarily.

    Following aspects covered without need for dedicated test cases:

        - dump
        - instantiating with class instances

    """

    expected_dump = Baseline(
        """
        +----------+---------+-------+-------------------+--------+
        | Offset   | Access  | Value | Bytes             | Format |
        +----------+---------+-------+-------------------+--------+
        | 0        |         | 46964 | 74 b7             | Outer  |
        |  [0:2]   | ol0     | 0     | ........ ......00 | int    |
        |  [2:4]   | ol1     | 1     | ........ ....01.. | int    |
        |          | ol2     |       |                   | Middle |
        |  [7]     |   ml0   | 0     | ........ 0....... | int    |
        |  [8]     |   ml1   | 1     | .......1 ........ | int    |
        |          |   ml2   |       |                   | Inner  |
        |  [11]    |     il0 | 0     | ....0... ........ | int    |
        |  [12]    |     il1 | 1     | ...1.... ........ | int    |
        |  [14:16] |     il2 | 2     | 10...... ........ | int    |
        +----------+---------+-------+-------------------+--------+
        """
    )

    def test_get(self):
        """Verify read access."""
        instance = Outer(
            ol0=0, ol1=1, ol2=Middle(ml0=0, ml1=1, ml2=Inner(il0=0, il1=1, il2=2))
        )

        assert instance == 0xB774

        assert instance.ol0 == 0
        assert instance.ol1 == 1
        assert instance.ol2 == 0x16E

        assert instance.ol2.ml0 == 0
        assert instance.ol2.ml1 == 1
        assert instance.ol2.ml2 == 0x16

        assert instance.ol2.ml2.il0 == 0
        assert instance.ol2.ml2.il1 == 1
        assert instance.ol2.ml2.il2 == 2

        assert str(instance.dump) == self.expected_dump

    def test_set(self):
        """Verify write access."""
        # initialize all fields to zero (except initialize to 1 all fields that
        # should be 0)
        instance = Outer(
            ol0=1, ol1=0, ol2=Middle(ml0=1, ml1=0, ml2=Inner(il0=1, il1=0, il2=0))
        )

        # fill in each field with expected value
        instance.ol0 = 0
        instance.ol1 = 1
        instance.ol2.ml0 = 0
        instance.ol2.ml1 = 1
        instance.ol2.ml2.il0 = 0
        instance.ol2.ml2.il1 = 1
        instance.ol2.ml2.il2 = 2

        assert str(instance.dump) == self.expected_dump

    def test_ignore_fields(self):
        """Verify ignored fields at lower level don't cause mis-compare.

        Verify bitfield(..., ignore=True) has impact from nested levels.

        """
        item1 = Outer(
            ol0=0, ol1=1, ol2=Middle(ml0=0, ml1=1, ml2=Inner(il0=0, il1=1, il2=2))
        )
        item2 = Outer(
            ol0=3, ol1=1, ol2=Middle(ml0=1, ml1=1, ml2=Inner(il0=1, il1=1, il2=2))
        )
        assert item1 == item2

    def test_ignore_background(self):
        """Verify ignored background bits at lower level don't cause mis-compare.

        Verify Middle(..., ignore=0x4) has impact.

        """
        assert Outer.from_int(0x210) == Outer.from_int(0)

    def test_fill(self):
        """Verify fill patterns for each class are meshed properly."""

        expected_dump = Baseline(
            """
            +----------+---------+-------+-------------------+--------+
            | Offset   | Access  | Value | Bytes             | Format |
            +----------+---------+-------+-------------------+--------+
            | 0        |         | 9840  | 70 26             | Outer  |
            |  [0:2]   | ol0     | 0     | ........ ......00 | int    |
            |  [2:4]   | ol1     | 0     | ........ ....00.. | int    |
            |          | ol2     |       |                   | Middle |
            |  [7]     |   ml0   | 0     | ........ 0....... | int    |
            |  [8]     |   ml1   | 0     | .......0 ........ | int    |
            |          |   ml2   |       |                   | Inner  |
            |  [11]    |     il0 | 0     | ....0... ........ | int    |
            |  [12]    |     il1 | 0     | ...0.... ........ | int    |
            |  [14:16] |     il2 | 0     | 00...... ........ | int    |
            +----------+---------+-------+-------------------+--------+
            """
        )

        instance = Outer(
            ol0=0, ol1=0, ol2=Middle(ml0=0, ml1=0, ml2=Inner(il0=0, il1=0, il2=0))
        )

        assert str(instance.dump) == expected_dump

    def test_repr(self):
        """Test representation."""
        instance = Outer(
            ol0=0, ol1=0, ol2=Middle(ml0=0, ml1=0, ml2=Inner(il0=0, il1=0, il2=0))
        )

        expected_repr = Baseline(
            """
            Outer(ol0=0, ol1=0, ol2=Middle(ml0=0, ml1=0, ml2=Inner(il0=0, il1=0, il2=0)))
            """
        )

        assert repr(instance) == expected_repr
        assert str(instance) == expected_repr


class TestGetterOptimization:

    """Test elimination of lsb added to bit offset in getter."""

    def test_getter(self):
        class Nested(BitFields, nested=True, fieldorder="least_to_most"):
            n1: int = bitfield(size=2)
            n2: int = bitfield(size=2)

        class Outside(BitFields, fieldorder="least_to_most"):
            o1: Nested = bitfield(size=4, typ=Nested)
            o2: int = bitfield(size=4)

        bitfields = Outside.from_int(3)

        assert bitfields.o1.n1 == 3
