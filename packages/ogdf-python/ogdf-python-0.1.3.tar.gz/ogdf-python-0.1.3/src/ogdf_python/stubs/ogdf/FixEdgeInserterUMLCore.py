# file stubs/ogdf/FixEdgeInserterUMLCore.py generated from classogdf_1_1_fix_edge_inserter_u_m_l_core
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
class FixEdgeInserterUMLCore(ogdf.FixEdgeInserterCore):

	#: true iff corresponding primal edge is a generalization.
	m_primalIsGen : EdgeArray[ bool ] = ...

	m_typeOfCurrentEdge : Graph.EdgeType = ...

	def __init__(self, pr : PlanRepLight, pCostOrig : EdgeArray[  int ], pEdgeSubgraph : EdgeArray[  int ]) -> None:
		...

	@overload
	def appendCandidates(self, nodesAtDist : Array[SListPure[edge] ], costDual : EdgeArray[  int ], maxCost : int, v : node, currentDist : int) -> None:
		...

	@overload
	def appendCandidates(self, queue : QueuePure[edge], v : node) -> None:
		...

	def cleanup(self) -> None:
		...

	def constructDual(self, E : CombinatorialEmbedding) -> None:
		...

	def init(self, E : CombinatorialEmbedding) -> None:
		...

	def insertEdgesIntoDual(self, E : CombinatorialEmbedding, adjSrc : adjEntry) -> None:
		...

	def insertEdgesIntoDualAfterRemove(self, E : CombinatorialEmbedding, f : face) -> None:
		...

	def storeTypeOfCurrentEdge(self, eOrig : edge) -> None:
		...
