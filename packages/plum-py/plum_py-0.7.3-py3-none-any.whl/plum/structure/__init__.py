# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# Copyright 2021 Daniel Mark Gass, see __about__.py for license information.
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
"""Structure of uniquely named and typed members data store and transform."""

from ._bitfield_member import bitfield_member
from ._dimmed_member import dimmed_member
from ._member import member
from ._meta import StructureMeta
from ._sized_member import sized_member
from ._structure import Structure

bitfield_member.__module__ = "plum.structure"
dimmed_member.__module__ = "plum.structure"
member.__module__ = "plum.structure"
StructureMeta.__module__ = "plum.structure"
sized_member.__module__ = "plum.structure"
Structure.__module__ = "plum.structure"
