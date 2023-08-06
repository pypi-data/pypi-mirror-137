# file stubs/ogdf/VarEdgeInserterUMLCore/BiconnectedComponentUML.py generated from classogdf_1_1_var_edge_inserter_u_m_l_core_1_1_biconnected_component_u_m_l
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
class BiconnectedComponentUML(ogdf.VarEdgeInserterCore.BiconnectedComponent):

	m_pr : PlanRepLight = ...

	def __init__(self, pr : PlanRepLight) -> None:
		...

	def typeOf(self, e : edge) -> EdgeType:
		...
