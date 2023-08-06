# file stubs/ogdf/Clusterer.py generated from classogdf_1_1_clusterer
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
class Clusterer(ogdf.ClustererModule):

	"""Clustering is determined based on the threshold values (connectivity thresholds determine edges to be deleted) and stopped if average clustering index drops below m_stopIndex."""

	m_autoThreshNum : int = ...

	m_autoThresholds : List[ float ] = ...

	m_defaultThresholds : List[ float ] = ...

	m_edgeValue : EdgeArray[ float ] = ...

	m_recursive : bool = ...

	m_stopIndex : float = ...

	m_thresholds : List[ float ] = ...

	m_vertexValue : NodeArray[ float ] = ...

	@overload
	def __init__(self) -> None:
		"""Default constructor allowing to cluster multiple graphs with the same instance of theClusterergraphs."""
		...

	@overload
	def __init__(self, G : Graph) -> None:
		"""Constructor taking a graph G to be clustered."""
		...

	def __destruct__(self) -> None:
		...

	@overload
	def computeCIndex(self, G : Graph, v : node) -> float:
		"""compute a clustering index for each vertex"""
		...

	@overload
	def computeCIndex(self, v : node) -> float:
		"""compute a clustering index for each vertex"""
		...

	def computeClustering(self, sl : SList[SimpleCluster]) -> None:
		"""compute some kind of clustering on the graph m_pGraph"""
		...

	@overload
	def computeEdgeStrengths(self, G : Graph, strength : EdgeArray[ float ]) -> None:
		...

	@overload
	def computeEdgeStrengths(self, strength : EdgeArray[ float ]) -> None:
		...

	def createClusterGraph(self, C : ClusterGraph) -> None:
		"""translate computed clustering into cluster hierarchy in cluster graph C"""
		...

	def setAutomaticThresholds(self, numValues : int) -> None:
		...

	def setClusteringThresholds(self, threshs : List[ float ]) -> None:
		...

	def setRecursive(self, b : bool) -> None:
		...

	def setStopIndex(self, stop : float) -> None:
		...
