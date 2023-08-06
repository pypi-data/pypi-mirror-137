# file stubs/ogdf/ModifiedNibbleClusterer.py generated from classogdf_1_1_modified_nibble_clusterer
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
class ModifiedNibbleClusterer(object):

	"""The modified nibble clustering algorithm."""

	class StartNodeStrategy(enum.Enum):

		MinDeg = enum.auto()

		MaxDeg = enum.auto()

		Random = enum.auto()

	def __init__(self) -> None:
		...

	def __destruct__(self) -> None:
		...

	@overload
	def call(self, G : Graph, clusterNum : NodeArray[  int ]) -> int:
		"""Call method: Creates a clustering of G Returns number of created clusters and sets cluster index for each node in clusterNum."""
		...

	@overload
	def call(self, G : Graph, clusterNum : NodeArray[  int ], topLevelNum : NodeArray[  int ]) -> int:
		"""A convenience method. Due to the characteristics of the algorithm (not very accurate, fast for large graphs), we could have a medium number (several hundreds) of clusters, and could need a further level of clustering. On the other hand, fully recursive clustering does not make much sense as after a second level there will be not to many clusters left. topLevelNum keeps a cluster number in the top level of the two level cluster hierarchy."""
		...

	def setClusterSizeThreshold(self, threshold : int) -> None:
		...

	def setMaxClusterNum(self, i : int) -> None:
		"""Call method: Creates a clustering of G in C Returns number of created clusters."""
		...

	def setMaxClusterSize(self, i : int) -> None:
		...

	def activeNodeBound(self) -> int:
		...

	def aPGP(self, i : int) -> int:
		...

	def findBestCluster(self, isActive : NodeArray[ bool ], activeNodes : List[node], cluster : List[node]) -> float:
		...

	def initialize(self) -> None:
		"""Initialize before FIRST step."""
		...

	def maxClusterSize(self) -> int:
		...

	def modifiedNibble(self, snode : node, bestCluster : List[node]) -> None:
		"""main step with walks starting from snode"""
		...

	def postProcess(self) -> None:
		...

	def pot(self, r : float, i : int) -> float:
		...

	def selectStartNode(self) -> node:
		"""select start node according to some strategy"""
		...

	def spreadValues(self, isActive : NodeArray[ bool ], activeNodes : List[node], probUpdate : NodeArray[ float ]) -> None:
		...
