# file stubs/ogdf/ClustererModule.py generated from classogdf_1_1_clusterer_module
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
class ClustererModule(object):

	"""Interface for algorithms that compute a clustering for a given graph."""

	m_pGraph : Graph = ...

	@overload
	def __init__(self) -> None:
		"""Default constructor, initializes a clustering module."""
		...

	@overload
	def __init__(self, G : Graph) -> None:
		...

	@overload
	def averageCIndex(self) -> float:
		"""compute the average clustering index for the given graph"""
		...

	@overload
	def averageCIndex(self, G : Graph) -> float:
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

	def createClusterGraph(self, C : ClusterGraph) -> None:
		"""translate computed clustering into cluster hierarchy in cluster graph C"""
		...

	def getGraph(self) -> Graph:
		"""Returns the graph to be clustered."""
		...

	def setGraph(self, G : Graph) -> None:
		"""Sets the graph to be clustered."""
		...
