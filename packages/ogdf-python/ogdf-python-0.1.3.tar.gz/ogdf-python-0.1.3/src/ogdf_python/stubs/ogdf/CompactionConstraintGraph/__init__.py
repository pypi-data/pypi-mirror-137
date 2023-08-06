# file stubs/ogdf/CompactionConstraintGraph/__init__.py generated from classogdf_1_1_compaction_constraint_graph
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
ATYPE = TypeVar('ATYPE')

class CompactionConstraintGraph(ogdf.CompactionConstraintGraphBase, Generic[ATYPE]):

	"""Represents a constraint graph used for compaction."""

	# Cost settings

	def __init__(self, OR : OrthoRep, PG : PlanRep, arcDir : OrthoDir, sep : ATYPE, costGen : int = 1, costAssoc : int = 1, align : bool = False) -> None:
		"""Construction."""
		...

	def areMulti(self, e1 : edge, e2 : edge) -> bool:
		"""Return PG result for flowcompaction."""
		...

	@overload
	def centerPriority(self) -> bool:
		"""Gets centerPriority (center single edges?)"""
		...

	@overload
	def centerPriority(self, b : bool) -> None:
		"""Sets centerPriority (center single edges?)"""
		...

	def computeTotalCosts(self, pos : NodeArray[ ATYPE ]) -> ATYPE:
		"""Computes the total costs for coordintes given by pos, i.e., the sum of the weighted lengths of edges in the constraint graph."""
		...

	def extraOfs(self, v : node) -> ATYPE:
		"""Returns extraNode position, change to save mem, only need some entries."""
		...

	@overload
	def insertVertexSizeArcs(self, PG : PlanRep, sizeOrig : NodeArray[ ATYPE ], minDist : MinimumEdgeDistances[ ATYPE ]) -> None:
		"""Inserts arcs for respecting sizes of vertices and achieving desired placement of generalizations if vertices are represented by tight cages. Also corrects length of arcs belonging to cages which are adjacent to a corner; takes special distances between edge segments attached at a vertex (delta's and epsilon's) into account."""
		...

	@overload
	def insertVertexSizeArcs(self, PG : PlanRep, sizeOrig : NodeArray[ ATYPE ], rc : RoutingChannel[ ATYPE ]) -> None:
		"""Inserts arcs for respecting sizes of vertices and achieving desired placement of generalizations if vertices are represented by variable cages; also corrects length of arcs belonging to cages which are adjacent to a corner; takes routing channels into account."""
		...

	@overload
	def insertVisibilityArcs(self, PG : PlanRep, posDir : NodeArray[ ATYPE ], posOppDir : NodeArray[ ATYPE ]) -> None:
		"""Inserts arcs connecting segments which can see each other in a drawing of the associated planarized representation PG which is given by posDir and posOppDir."""
		...

	@overload
	def insertVisibilityArcs(self, PG : PlanRep, posDir : NodeArray[ ATYPE ], posOrthDir : NodeArray[ ATYPE ], minDist : MinimumEdgeDistances[ ATYPE ]) -> None:
		...

	def isFeasible(self, pos : NodeArray[ ATYPE ]) -> bool:
		"""Performs feasibility test for position assignment pos, i.e., checks if the segment positions given by pos fulfill the constraints in the compaction constraint graph (for debuging only)"""
		...

	def length(self, e : edge) -> ATYPE:
		"""Returns length of edgee."""
		...

	def separation(self) -> ATYPE:
		"""Returns the separation value."""
		...

	def setMinimumSeparation(self, PG : PlanRep, coord : NodeArray[  int ], minDist : MinimumEdgeDistances[ ATYPE ]) -> None:
		"""Sets min separation for multi edge original."""
		...

	def initializeCosts(self) -> None:
		...

	def setExtra(self, v : node, rep : node, ofs : ATYPE) -> None:
		"""Nodevhas no representation in drawing, only internal representation."""
		...
