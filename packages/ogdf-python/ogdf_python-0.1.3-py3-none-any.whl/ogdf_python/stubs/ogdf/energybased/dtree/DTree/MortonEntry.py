# file stubs/ogdf/energybased/dtree/DTree/MortonEntry.py generated from structogdf_1_1energybased_1_1dtree_1_1_d_tree_1_1_morton_entry
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
class MortonEntry(object):

	"""The entry in the sorted order for a point."""

	#: the morton number of the point
	mortonNr : IntType = ...

	#: index in the original point order
	ref : int = ...

	def __lt__(self, other : MortonEntry) -> bool:
		"""less comparator for sort"""
		...

	def __eq__(self, other : MortonEntry) -> bool:
		"""equal comparer for the construction algorithm"""
		...
