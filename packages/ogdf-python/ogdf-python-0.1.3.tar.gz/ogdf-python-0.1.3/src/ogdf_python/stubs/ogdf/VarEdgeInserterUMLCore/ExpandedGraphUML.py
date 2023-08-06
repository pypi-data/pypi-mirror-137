# file stubs/ogdf/VarEdgeInserterUMLCore/ExpandedGraphUML.py generated from classogdf_1_1_var_edge_inserter_u_m_l_core_1_1_expanded_graph_u_m_l
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
class ExpandedGraphUML(ogdf.VarEdgeInserterCore.ExpandedGraph):

	m_primalIsGen : EdgeArray[ bool ] = ...

	def __init__(self, BC : BiconnectedComponentUML, T : StaticSPQRTree, gc : GraphCopy) -> None:
		...

	def __destruct__(self) -> None:
		...

	def constructDual(self, s : node, t : node) -> None:
		...

	@overload
	def appendCandidates(self, nodesAtDist : Array[SListPure[edge] ], maxCost : int, v : node, eType : Graph.EdgeType, currentDist : int) -> None:
		...

	@overload
	def appendCandidates(self, queue : List[edge], v : node, eType : Graph.EdgeType) -> None:
		...
