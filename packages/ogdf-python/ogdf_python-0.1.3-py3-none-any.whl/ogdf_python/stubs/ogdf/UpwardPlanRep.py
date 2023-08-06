# file stubs/ogdf/UpwardPlanRep.py generated from classogdf_1_1_upward_plan_rep
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
class UpwardPlanRep(ogdf.GraphCopy):

	"""Upward planarized representations (of a connected component) of a graph."""

	crossings : int = ...

	extFaceHandle : adjEntry = ...

	#: theUpwardPlanRepis augmented to a single source and single sink graph
	isAugmented : bool = ...

	m_Gamma : CombinatorialEmbedding = ...

	m_isSinkArc : EdgeArray[ bool ] = ...

	m_isSourceArc : EdgeArray[ bool ] = ...

	m_sinkSwitchOf : NodeArray[adjEntry] = ...

	#: the super source
	s_hat : node = ...

	#: < embedding og thisUpwardPlanRep
	t_hat : node = ...

	@overload
	def __init__(self) -> None:
		"""standart constructor"""
		...

	@overload
	def __init__(self, Gamma : CombinatorialEmbedding) -> None:
		...

	@overload
	def __init__(self, GC : GraphCopy, adj_ext : adjEntry) -> None:
		...

	@overload
	def __init__(self, UPR : UpwardPlanRep) -> None:
		"""copy constructor"""
		...

	def __destruct__(self) -> None:
		...

	def augment(self) -> None:
		"""convert to a single source single sink graph (result is not necessary a st-graph!)."""
		...

	def augmented(self) -> bool:
		"""return true if graph is augmented to a single source single sink graph"""
		...

	def getAdjEntry(self, Gamma : CombinatorialEmbedding, v : node, f : face) -> adjEntry:
		"""return the adjEntry of v which right face is f."""
		...

	@overload
	def getEmbedding(self) -> CombinatorialEmbedding:
		...

	@overload
	def getEmbedding(self) -> CombinatorialEmbedding:
		"""return the upward planar embedding"""
		...

	def getSuperSink(self) -> node:
		...

	def getSuperSource(self) -> node:
		...

	def insertEdgePathEmbedded(self, eOrig : edge, crossedEdges : SList[adjEntry], cost : EdgeArray[  int ]) -> None:
		"""same as insertEdgePath, but assumes that the graph is embedded"""
		...

	def isSinkArc(self, e : edge) -> bool:
		...

	def isSourceArc(self, e : edge) -> bool:
		...

	def leftInEdge(self, v : node) -> adjEntry:
		...

	def numberOfCrossings(self) -> int:
		...

	def __assign__(self, copy : UpwardPlanRep) -> UpwardPlanRep:
		"""Assignment operator."""
		...

	def outputFaces(self, embedding : CombinatorialEmbedding) -> None:
		...

	def sinkSwitchOf(self, v : node) -> adjEntry:
		"""0 if node v is not a sink switch (not the top sink switch !!) of an internal face. else v is sink-switch of the right face of the adjEntry."""
		...
