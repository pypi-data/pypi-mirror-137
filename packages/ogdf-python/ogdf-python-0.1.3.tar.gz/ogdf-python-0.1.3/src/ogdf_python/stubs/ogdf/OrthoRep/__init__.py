# file stubs/ogdf/OrthoRep/__init__.py generated from classogdf_1_1_ortho_rep
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
class OrthoRep(object):

	"""Orthogonal representation of an embedded graph."""

	@overload
	def __init__(self) -> None:
		...

	@overload
	def __init__(self, E : CombinatorialEmbedding) -> None:
		...

	def __destruct__(self) -> None:
		...

	def alignAdjEntry(self) -> adjEntry:
		...

	@overload
	def angle(self, adj : adjEntry) -> int:
		...

	@overload
	def angle(self, adj : adjEntry) -> int:
		...

	@overload
	def bend(self, adj : adjEntry) -> BendString:
		...

	@overload
	def bend(self, adj : adjEntry) -> BendString:
		...

	@overload
	def cageInfo(self, v : node) -> VertexInfoUML:
		...

	@overload
	def cageInfo(self, v : node) -> VertexInfoUML:
		...

	def check(self, error : str) -> bool:
		...

	def computeCageInfoUML(self, PG : PlanRep) -> None:
		...

	def direction(self, adj : adjEntry) -> OrthoDir:
		...

	def dissect(self) -> None:
		...

	def dissect2(self, PG : PlanRep = None) -> None:
		...

	def externalAdjEntry(self) -> adjEntry:
		...

	def gridDissect(self, PG : PlanRep) -> None:
		...

	def init(self, E : CombinatorialEmbedding) -> None:
		...

	def isNormalized(self) -> bool:
		...

	def isOrientated(self) -> bool:
		...

	def normalize(self) -> None:
		...

	def __CombinatorialEmbedding__(self) -> None:
		...

	def __Graph__(self) -> None:
		...

	@overload
	def orientate(self) -> None:
		...

	@overload
	def orientate(self, adj : adjEntry, dir : OrthoDir) -> None:
		...

	@overload
	def orientate(self, PG : PlanRep, preferedDir : OrthoDir) -> None:
		...

	def rotate(self, r : int) -> None:
		...

	def undissect(self, align : bool = False) -> None:
		...

	def flip(self, c : int) -> int:
		...

	def nextDir(self, d : OrthoDir) -> OrthoDir:
		"""Returns the next OrthoDir (in a clockwise manner)"""
		...

	def oppDir(self, d : OrthoDir) -> OrthoDir:
		"""Returns the opposite OrthoDir."""
		...

	def prevDir(self, d : OrthoDir) -> OrthoDir:
		"""Returns the previous OrthoDir (in a clockwise manner)"""
		...
