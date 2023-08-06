# file stubs/ogdf/CommonCompactionConstraintGraphBase.py generated from classogdf_1_1_common_compaction_constraint_graph_base
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
class CommonCompactionConstraintGraphBase(ogdf.Graph):

	"""A common base class forogdf::GridCompactionConstraintGraphBaseandogdf::CompactionConstraintGraphBase."""

	@overload
	def getGraph(self) -> Graph:
		"""Returns underlying graph."""
		...

	@overload
	def getGraph(self) -> Graph:
		...

	def getOrthoRep(self) -> OrthoRep:
		"""Returns underlyingOrthoRep."""
		...

	def getPlanRep(self) -> PlanRep:
		...

	def nodesIn(self, v : node) -> SListPure[node]:
		"""Returns list of nodes contained in segmentv."""
		...

	def pathNodeOf(self, v : node) -> node:
		"""Returns the segment (path node in constraint graph) containingv."""
		...

	def cost(self, e : edge) -> int:
		"""Returns cost of edgee."""
		...

	def extraRep(self, v : node) -> node:
		"""Returns extraNode existing anchor representant."""
		...

	def onBorder(self, e : edge) -> bool:
		"""Returns true if edge lies on cage border."""
		...

	def fixOnBorder(self, e : edge) -> bool:
		"""Returns true if edge is subject to length fixation if length < sep."""
		...

	m_arcDir : OrthoDir = ...

	#: only used for cage precompaction in flowcompaction computecoords
	m_border : EdgeArray[  int ] = ...

	#: cost of an edge
	m_cost : EdgeArray[  int ] = ...

	#: basic arc representing an edge in PG
	m_edgeToBasicArc : EdgeArray[edge] = ...

	#: Node does not represent drawing node as we dont have positions we save a drawing representant and an offset.
	m_extraNode : NodeArray[ bool ] = ...

	#: existing representant of extranodes position anchor
	m_extraRep : NodeArray[node] = ...

	m_oppArcDir : OrthoDir = ...

	#: save edge for the basic arcs
	m_originalEdge : NodeArray[edge] = ...

	#: list of nodes contained in a segment
	m_path : NodeArray[SListPure[node] ] = ...

	#: segment containing a node in PG
	m_pathNode : NodeArray[node] = ...

	m_pOR : OrthoRep = ...

	m_pPR : PlanRep = ...

	m_sinks : SList[node] = ...

	m_sources : SList[node] = ...

	#: constraint type for each edge
	m_type : EdgeArray[ConstraintEdgeType] = ...

	def __init__(self, OR : OrthoRep, PG : PlanRep, arcDir : OrthoDir, costAssoc : int) -> None:
		"""Build constraint graph with basic arcs."""
		...

	def getLengthString(self, e : edge) -> str:
		...

	def basicArc(self, e : edge) -> edge:
		"""Returns constraint arc representing input edge e in constraint graph."""
		...

	def computeTopologicalSegmentNum(self, topNum : NodeArray[  int ]) -> None:
		"""Computes topological numbering on the segments of the constraint graph."""
		...

	def embed(self) -> None:
		"""Embeds constraint graph such that all sources and sinks lie in a common face."""
		...

	def extraNode(self, v : node) -> bool:
		"""Returns node status."""
		...

	def removeRedundantVisibArcs(self, visibArcs : SListPure[Tuple2[node,node]]) -> None:
		"""Removes "arcs" fromvisibArcswhich we already have in the constraint graph (as basic arcs)"""
		...

	def typeOf(self, e : edge) -> ConstraintEdgeType:
		"""Returns type of edgee."""
		...
