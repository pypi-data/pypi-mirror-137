# file stubs/ogdf/Dijkstra.py generated from classogdf_1_1_dijkstra
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
H = TypeVar('H')

T = TypeVar('T')

class Dijkstra(Generic[T, H]):

	"""Dijkstra's single source shortest path algorithm."""

	#: For floating point comparisons (if floating point is used)
	m_eps : EpsilonTest = ...

	@overload
	def call(self, G : Graph, weight : EdgeArray[ T ], sources : List[node], predecessor : NodeArray[edge], distance : NodeArray[ T ], directed : bool = False, target : node = None, maxLength : T = std.numeric_limits[ T ].max()) -> None:
		"""Calculates, based on the graph G with corresponding edge costs and source nodes, the shortest paths and distances to all other nodes byDijkstra's algorithm."""
		...

	@overload
	def call(self, G : Graph, weight : EdgeArray[ T ], s : node, predecessor : NodeArray[edge], distance : NodeArray[ T ], directed : bool = False, target : node = None, maxLength : T = std.numeric_limits[ T ].max()) -> None:
		"""Calculates, based on the graph G with corresponding edge costs and a source node s, the shortest paths and distances to all other nodes byDijkstra's algorithm."""
		...

	@overload
	def callBound(self, G : Graph, weight : EdgeArray[ T ], sources : List[node], predecessor : NodeArray[edge], distance : NodeArray[ T ], directed : bool, target : node, maxLength : T = std.numeric_limits[ T ].max()) -> None:
		"""Calculates, based on the graph G with corresponding edge costs and source nodes, the shortest paths and distances to all other nodes byDijkstra's algorithm."""
		...

	@overload
	def callBound(self, G : Graph, weight : EdgeArray[ T ], s : node, predecessor : NodeArray[edge], distance : NodeArray[ T ], directed : bool, target : node, maxLength : T = std.numeric_limits[ T ].max()) -> None:
		"""Calculates, based on the graph G with corresponding edge costs and a source node s, the shortest paths and distances to all other nodes byDijkstra's algorithm."""
		...

	@overload
	def callUnbound(self, G : Graph, weight : EdgeArray[ T ], sources : List[node], predecessor : NodeArray[edge], distance : NodeArray[ T ], directed : bool = False) -> None:
		"""Calculates, based on the graph G with corresponding edge costs and source nodes, the shortest paths and distances to all other nodes byDijkstra's algorithm."""
		...

	@overload
	def callUnbound(self, G : Graph, weight : EdgeArray[ T ], s : node, predecessor : NodeArray[edge], distance : NodeArray[ T ], directed : bool = False) -> None:
		"""Calculates, based on the graph G with corresponding edge costs and a source node s, the shortest paths and distances to all other nodes byDijkstra's algorithm."""
		...
