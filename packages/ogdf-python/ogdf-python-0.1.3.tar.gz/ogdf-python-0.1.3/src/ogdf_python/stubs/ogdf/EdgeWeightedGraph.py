# file stubs/ogdf/EdgeWeightedGraph.py generated from classogdf_1_1_edge_weighted_graph
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
T = TypeVar('T')

class EdgeWeightedGraph(ogdf.Graph, Generic[T]):

	m_edgeWeight : EdgeArray[ T ] = ...

	@overload
	def __init__(self) -> None:
		...

	@overload
	def __init__(self, gC : GraphCopy) -> None:
		...

	def __destruct__(self) -> None:
		...

	def edgeWeights(self) -> EdgeArray[ T ]:
		...

	def newEdge(self, v : node, w : node, weight : T) -> edge:
		...

	def newNode(self) -> node:
		...

	def setWeight(self, e : edge, weight : T) -> None:
		...

	def weight(self, e : edge) -> T:
		...
