# file stubs/ogdf/VarEdgeInserterDynUMLCore/__init__.py generated from classogdf_1_1_var_edge_inserter_dyn_u_m_l_core
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
class VarEdgeInserterDynUMLCore(ogdf.VarEdgeInserterDynCore):

	m_typeOfCurrentEdge : Graph.EdgeType = ...

	def __init__(self, pr : PlanRepLight, pCostOrig : EdgeArray[  int ], pEdgeSubgraph : EdgeArray[  int ]) -> None:
		...

	def buildSubpath(self, v : node, vPred : node, vSucc : node, L : List[adjEntry], Exp : ExpandedGraph, s : node, t : node) -> None:
		...

	def createBCandSPQRtrees(self) -> BCandSPQRtrees:
		...

	def createExpandedGraph(self, BC : BCandSPQRtrees) -> ExpandedGraph:
		...

	def storeTypeOfCurrentEdge(self, eOrig : edge) -> None:
		...
