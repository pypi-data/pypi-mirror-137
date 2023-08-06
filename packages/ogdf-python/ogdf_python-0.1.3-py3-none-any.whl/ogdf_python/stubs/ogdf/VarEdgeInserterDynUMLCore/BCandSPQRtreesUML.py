# file stubs/ogdf/VarEdgeInserterDynUMLCore/BCandSPQRtreesUML.py generated from classogdf_1_1_var_edge_inserter_dyn_u_m_l_core_1_1_b_cand_s_p_q_rtrees_u_m_l
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
class BCandSPQRtreesUML(ogdf.VarEdgeInserterDynCore.BCandSPQRtrees):

	def __init__(self, pr : PlanRepLight, costOrig : EdgeArray[  int ]) -> None:
		...

	def insertEdgePath(self, eOrig : edge, crossedEdges : SList[adjEntry]) -> None:
		...

	@overload
	def typeOf(self, e : edge) -> Graph.EdgeType:
		...

	@overload
	def typeOf(self, e : edge, et : Graph.EdgeType) -> None:
		...
