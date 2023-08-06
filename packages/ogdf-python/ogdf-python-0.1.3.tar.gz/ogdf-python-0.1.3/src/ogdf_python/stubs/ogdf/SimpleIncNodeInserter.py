# file stubs/ogdf/SimpleIncNodeInserter.py generated from classogdf_1_1_simple_inc_node_inserter
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
class SimpleIncNodeInserter(ogdf.IncNodeInserter):

	def __init__(self, PG : PlanRepInc) -> None:
		...

	def __destruct__(self) -> None:
		...

	@overload
	def insertCopyNode(self, v : node, E : CombinatorialEmbedding, vTyp : Graph.NodeType) -> None:
		"""Inserts copy inm_planRepfor original nodev."""
		...

	@overload
	def insertCopyNode(self, v : node, vTyp : Graph.NodeType) -> None:
		...

	def constructDual(self, G : Graph, E : CombinatorialEmbedding, forbidCrossings : bool = True) -> None:
		...

	def findShortestPath(self, E : CombinatorialEmbedding, s : node, t : node, eType : Graph.EdgeType, crossed : SList[adjEntry]) -> None:
		...

	def getInsertionFace(self, v : node, E : CombinatorialEmbedding) -> face:
		"""Returns a face to insert a copy ofvand a list of adjacency entries corresponding to the insertion adjEntries for the adjacent edges."""
		...

	def insertCrossingEdges(self, v : node, vCopy : node, E : CombinatorialEmbedding, adExternal : adjEntry) -> None:
		...

	def insertEdge(self, E : CombinatorialEmbedding, eOrig : edge, crossed : SList[adjEntry], forbidCrossingGens : bool) -> None:
		...

	def insertFaceEdges(self, v : node, vCopy : node, f : face, E : CombinatorialEmbedding, adExternal : adjEntry) -> None:
		...
