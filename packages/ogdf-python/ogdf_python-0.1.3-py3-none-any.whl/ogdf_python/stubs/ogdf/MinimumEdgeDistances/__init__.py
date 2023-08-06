# file stubs/ogdf/MinimumEdgeDistances/__init__.py generated from classogdf_1_1_minimum_edge_distances
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
ATYPE = TypeVar('ATYPE')

class MinimumEdgeDistances(Generic[ATYPE]):

	"""Maintains input sizes for improvement compaction (deltas and epsilons)"""

	def __init__(self, G : Graph, sep : ATYPE) -> None:
		...

	@overload
	def delta(self, v : node, s : OrthoDir, i : int) -> ATYPE:
		...

	@overload
	def delta(self, v : node, s : OrthoDir, i : int) -> ATYPE:
		...

	@overload
	def epsilon(self, v : node, s : OrthoDir, i : int) -> ATYPE:
		...

	@overload
	def epsilon(self, v : node, s : OrthoDir, i : int) -> ATYPE:
		...

	@overload
	def separation(self) -> ATYPE:
		...

	@overload
	def separation(self, sep : ATYPE) -> None:
		...
