# file stubs/ogdf/VarEdgeInserterCore/BiconnectedComponent.py generated from classogdf_1_1_var_edge_inserter_core_1_1_biconnected_component
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
class BiconnectedComponent(ogdf.Graph):

	m_BCtoG : AdjEntryArray[adjEntry] = ...

	m_cost : EdgeArray[  int ] = ...

	def __init__(self) -> None:
		...

	@overload
	def cost(self, e : edge) -> int:
		...

	@overload
	def cost(self, e : edge, c : int) -> None:
		...
