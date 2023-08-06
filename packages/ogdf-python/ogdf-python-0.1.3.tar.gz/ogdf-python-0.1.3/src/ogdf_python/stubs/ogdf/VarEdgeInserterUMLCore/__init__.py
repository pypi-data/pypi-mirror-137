# file stubs/ogdf/VarEdgeInserterUMLCore/__init__.py generated from classogdf_1_1_var_edge_inserter_u_m_l_core
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
class VarEdgeInserterUMLCore(ogdf.VarEdgeInserterCore):

	m_typeOfCurrentEdge : Graph.EdgeType = ...

	def __init__(self, pr : PlanRepLight, pCostOrig : EdgeArray[  int ], pEdgeSubgraph : EdgeArray[  int ]) -> None:
		...

	def buildSubpath(self, v : node, eIn : edge, eOut : edge, L : List[adjEntry], Exp : ExpandedGraph, s : node, t : node) -> None:
		...

	def createBlock(self) -> BiconnectedComponent:
		...

	def createExpandedGraph(self, BC : BiconnectedComponent, T : StaticSPQRTree) -> ExpandedGraph:
		...

	def storeTypeOfCurrentEdge(self, eOrig : edge) -> None:
		...
