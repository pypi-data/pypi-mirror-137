# file stubs/ogdf/EdgeWeightedGraphCopy.py generated from classogdf_1_1_edge_weighted_graph_copy
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
T = TypeVar('T')

class EdgeWeightedGraphCopy(ogdf.GraphCopy, Generic[T]):

	m_edgeWeight : EdgeArray[ T ] = ...

	@overload
	def __init__(self) -> None:
		...

	@overload
	def __init__(self, wC : EdgeWeightedGraph[ T ]) -> None:
		...

	@overload
	def __init__(self, wGC : EdgeWeightedGraphCopy) -> None:
		...

	def __destruct__(self) -> None:
		...

	def createEmpty(self, wG : Graph) -> None:
		...

	def edgeWeights(self) -> EdgeArray[ T ]:
		...

	def init(self, wG : EdgeWeightedGraph[ T ]) -> None:
		...

	@overload
	def newEdge(self, eOrig : edge, weight : T) -> edge:
		...

	@overload
	def newEdge(self, u : node, v : node, weight : T) -> edge:
		...

	def __assign__(self, wGC : EdgeWeightedGraphCopy) -> EdgeWeightedGraphCopy:
		...

	def setWeight(self, e : edge, v : T) -> None:
		...

	def weight(self, e : edge) -> T:
		...
