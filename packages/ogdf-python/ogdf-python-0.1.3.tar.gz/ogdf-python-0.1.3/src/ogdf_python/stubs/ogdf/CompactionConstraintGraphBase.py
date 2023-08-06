# file stubs/ogdf/CompactionConstraintGraphBase.py generated from classogdf_1_1_compaction_constraint_graph_base
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
class CompactionConstraintGraphBase(ogdf.CommonCompactionConstraintGraphBase):

	"""Class implementing template-parameter-independent behaviour ofogdf::CompactionConstraintGraph."""

	# Edge property getters

	def verticalGen(self, e : edge) -> bool:
		"""Returns true if e is vertical edge inPlanRepUMLhierarchy."""
		...

	def verticalArc(self, e : edge) -> bool:
		"""Returns true if e is basic arc of vertical edge inPlanRepUMLhierarchy."""
		...

	#: Basic arcs that have to be short for alignment (node to gen expander)
	m_alignmentArc : EdgeArray[ bool ] = ...

	m_edgeCost : int = ...

	#: save the (single!) edge (segment) for a pathNode
	m_pathToEdge : NodeArray[edge] = ...

	#: arc corresponding to such an edge
	m_verticalArc : EdgeArray[ bool ] = ...

	#: generalization that runs vertical relative to hierarchy
	m_verticalGen : EdgeArray[ bool ] = ...

	def align(self, b : bool) -> None:
		"""Triggers alignment (=>some special edge handling to support al.)"""
		...

	def alignmentArc(self, e : edge) -> bool:
		"""Returns if arc is important for alignment. These are the arcs representing node to gen. merger edges."""
		...

	def pathToOriginal(self, v : node) -> edge:
		...

	def __init__(self, OR : OrthoRep, PG : PlanRep, arcDir : OrthoDir, costGen : int = 1, costAssoc : int = 1, align : bool = False) -> None:
		"""Construction."""
		...
