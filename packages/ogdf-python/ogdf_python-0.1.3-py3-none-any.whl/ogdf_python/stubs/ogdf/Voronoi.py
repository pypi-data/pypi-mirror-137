# file stubs/ogdf/Voronoi.py generated from classogdf_1_1_voronoi
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
T = TypeVar('T')

class Voronoi(Generic[T]):

	"""Computes Voronoi regions in an edge-weighted graph."""

	m_distance : NodeArray[ T ] = ...

	m_graph : Graph = ...

	m_nodeList : Dict[node,ArrayBuffer[node] ] = ...

	m_predecessor : NodeArray[edge] = ...

	m_seedOfNode : NodeArray[node] = ...

	m_seeds : List[node] = ...

	def computeVoronoiRegions(self, G : Graph, weights : EdgeArray[ T ], seeds : List[node]) -> None:
		...

	def __init__(self, G : Graph, weights : EdgeArray[ T ], seeds : List[node]) -> None:
		"""Build data structure to query Voronoi regions of edge-weighted graphGwith given Voronoi seeds."""
		...

	def distance(self, v : node) -> T:
		"""Returns the distance betweenvand its Voronoi seed."""
		...

	def getGraph(self) -> Graph:
		"""Returns a reference to the graph the Voronoi region has been computed for."""
		...

	def getSeeds(self) -> List[node]:
		"""Returns a reference to the list of seeds the Voronoi region has been computed for."""
		...

	def nodesInRegion(self, v : node) -> ArrayBuffer[node]:
		"""Returns the list of nodes in the Voronoi region of nodev."""
		...

	def predecessor(self, v : node) -> node:
		"""Returns the nearest node tovon the shortest path to its Voronoi seed."""
		...

	def predecessorEdge(self, v : node) -> edge:
		"""Returns the edge incident tovand its predecessor. Note that the predecessor of a terminal isnullptr."""
		...

	def seed(self, v : node) -> node:
		"""Returns the Voronoi seed of nodev."""
		...
