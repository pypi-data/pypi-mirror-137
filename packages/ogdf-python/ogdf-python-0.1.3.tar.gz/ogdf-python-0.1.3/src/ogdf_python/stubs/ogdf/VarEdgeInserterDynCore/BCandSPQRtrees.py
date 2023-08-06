# file stubs/ogdf/VarEdgeInserterDynCore/BCandSPQRtrees.py generated from classogdf_1_1_var_edge_inserter_dyn_core_1_1_b_cand_s_p_q_rtrees
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
class BCandSPQRtrees(object):

	m_cost : EdgeArray[  int ] = ...

	m_costOrig : EdgeArray[  int ] = ...

	m_dynamicSPQRForest : DynamicSPQRForest = ...

	m_pr : PlanRepLight = ...

	def __init__(self, pr : PlanRepLight, costOrig : EdgeArray[  int ]) -> None:
		...

	def __destruct__(self) -> None:
		...

	@overload
	def cost(self, e : edge) -> int:
		...

	@overload
	def cost(self, e : edge, c : int) -> None:
		...

	def dynamicSPQRForest(self) -> DynamicSPQRForest:
		...

	def insertEdgePath(self, eOrig : edge, crossedEdges : SList[adjEntry]) -> None:
		...
