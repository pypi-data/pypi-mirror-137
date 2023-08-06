# file stubs/ogdf/GridCompactionConstraintGraph/__init__.py generated from classogdf_1_1_grid_compaction_constraint_graph
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
ATYPE = TypeVar('ATYPE')

class GridCompactionConstraintGraph(ogdf.GridCompactionConstraintGraphBase, Generic[ATYPE]):

	"""Represents a constraint graph used for compaction."""

	# Cost settings

	def __init__(self, OR : OrthoRep, PG : PlanRep, arcDir : OrthoDir, sep : ATYPE) -> None:
		"""Construction."""
		...

	def areMulti(self, e1 : edge, e2 : edge) -> bool:
		"""Returns PG result for flowcompaction."""
		...

	def computeTotalCosts(self, pos : NodeArray[ ATYPE ]) -> ATYPE:
		"""Computes the total costs for coordintes given by pos, i.e., the sum of the weighted lengths of edges in the constraint graph."""
		...

	def extraOfs(self, v : node) -> ATYPE:
		"""Returns extraNode position, change to save mem, only need some entries."""
		...

	def insertVisibilityArcs(self, PG : PlanRep, posDir : NodeArray[ ATYPE ], posOrthDir : NodeArray[ ATYPE ]) -> None:
		"""Inserts arcs connecting segments which can see each other in a drawing of the associated planarized representation PG which is given by posDir and posOppDir."""
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
		"""Sets min sep for multi edge original."""
		...

	def initializeCosts(self) -> None:
		...

	def setExtra(self, v : node, rep : node, ofs : ATYPE) -> None:
		...
