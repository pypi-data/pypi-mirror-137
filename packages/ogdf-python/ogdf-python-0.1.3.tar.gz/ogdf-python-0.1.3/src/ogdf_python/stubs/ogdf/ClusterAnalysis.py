# file stubs/ogdf/ClusterAnalysis.py generated from classogdf_1_1_cluster_analysis
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
class ClusterAnalysis(object):

	DefaultIndex : int = ...

	IsNotActiveBound : int = ...

	@overload
	def __init__(self, C : ClusterGraph, indyBags : bool = False) -> None:
		"""Constructor. Performs all analyses and in case indyBags is set to true, also computes a partition into independently solvable subproblems for cluster planarization (if applicable)."""
		...

	@overload
	def __init__(self, C : ClusterGraph, oalists : bool, indyBags : bool) -> None:
		"""Additionally allows to forbid storing lists of outer active vertices."""
		...

	def __destruct__(self) -> None:
		...

	def bagIndex(self, v : node, c : cluster) -> int:
		"""Returns bag index number for a vertexvin clusterc."""
		...

	def indyBagIndex(self, v : node) -> int:
		"""Returns independent bag index number for a vertexv."""
		...

	def indyBagRoot(self, i : int) -> cluster:
		"""Returns root cluster of independent bag. Note that this cluster either has direct vertex members or more than one child."""
		...

	def innerActive(self, c : cluster) -> int:
		"""Returns number of inneractive vertices of cluster c."""
		...

	def isInnerActive(self, v : node, c : cluster) -> bool:
		...

	def isOuterActive(self, v : node, c : cluster) -> bool:
		"""Returns outer activity status for vertexvwrt clusterc."""
		...

	def lcaEdges(self, c : cluster) -> List[edge]:
		"""Returns list of edges for cluster c with lca c."""
		...

	def minIALevel(self, v : node) -> int:
		"""Returns the highest (smallest) level depth for which a vertex is inner active, only initialized if vertex is inner active."""
		...

	def minIOALevel(self, v : node) -> int:
		"""Returns the highest (smallest) level depth for which a vertex is inner or outer active."""
		...

	def minOALevel(self, v : node) -> int:
		"""Returns the highest (smallest) level depth for which a vertex is outer active, only initialized if vertex is outer active."""
		...

	def numberOfBags(self, c : cluster) -> int:
		"""Returns number of bags for clusterc."""
		...

	def numberOfIndyBags(self) -> int:
		"""Returns number of independent bags in clustergraph, -1 in case no independent bags were computed. Ascending consecutive numbers are assigned, starting from 0."""
		...

	def oaNodes(self, c : cluster) -> List[node]:
		"""Returns list of outeractive vertices for clusterc. The result is only valid if lists are stored, i.e. m_storeoalists is true."""
		...

	def outerActive(self, c : cluster) -> int:
		"""Returns number of outeractive vertices of cluster c."""
		...

	def computeBags(self) -> None:
		"""Compute bags per cluster and store result as vertex-bag index in m_bagIndex."""
		...

	def computeIndyBags(self) -> None:
		"""Compute independent bags per cluster and store result as vertex-indyBag index in m_indyBagNumber."""
		...
