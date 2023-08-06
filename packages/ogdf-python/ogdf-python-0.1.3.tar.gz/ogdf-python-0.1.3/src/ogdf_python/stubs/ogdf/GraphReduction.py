# file stubs/ogdf/GraphReduction.py generated from classogdf_1_1_graph_reduction
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
class GraphReduction(ogdf.Graph):

	"""Creates a reduced graph by removing leaves, self-loops, and reducing chains."""

	m_eOrig : EdgeArray[List[edge] ] = ...

	m_eReduction : EdgeArray[edge] = ...

	m_pGraph : Graph = ...

	m_vOrig : NodeArray[node] = ...

	m_vReduction : NodeArray[node] = ...

	@overload
	def __init__(self) -> None:
		...

	@overload
	def __init__(self, G : Graph) -> None:
		...

	def __destruct__(self) -> None:
		...

	@overload
	def original(self) -> Graph:
		...

	@overload
	def original(self, e : edge) -> List[edge]:
		...

	@overload
	def original(self, v : node) -> node:
		...

	@overload
	def reduction(self, e : edge) -> edge:
		...

	@overload
	def reduction(self, v : node) -> node:
		...
