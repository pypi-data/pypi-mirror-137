# file stubs/ogdf/ClusterPlanRep.py generated from classogdf_1_1_cluster_plan_rep
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
class ClusterPlanRep(ogdf.PlanRep):

	"""Planarized representations for clustered graphs."""

	def __init__(self, acGraph : ClusterGraphAttributes, clusterGraph : ClusterGraph) -> None:
		...

	def __destruct__(self) -> None:
		...

	@overload
	def ClusterID(self, e : edge) -> int:
		...

	@overload
	def ClusterID(self, v : node) -> int:
		...

	def clusterOfDummy(self, v : node) -> cluster:
		...

	def clusterOfEdge(self, e : edge) -> cluster:
		"""Returns cluster of edgee."""
		...

	def clusterOfIndex(self, i : int) -> cluster:
		...

	def expand(self, lowDegreeExpand : bool = False) -> None:
		"""Expands nodes with degree > 4 and merge nodes for generalizations."""
		...

	def expandLowDegreeVertices(self, OR : OrthoRep) -> None:
		...

	def externalAdj(self) -> adjEntry:
		...

	def getClusterGraph(self) -> ClusterGraph:
		...

	def initCC(self, i : int) -> None:
		...

	def insertEdgePathEmbedded(self, eOrig : edge, E : CombinatorialEmbedding, crossedEdges : SList[adjEntry]) -> None:
		"""re-inserts edge eOrig by "crossing" the edges in crossedEdges; splits each edge in crossedEdges Precond."""
		...

	def isClusterBoundary(self, e : edge) -> bool:
		...

	def ModelBoundaries(self) -> None:
		...

	def setClusterBoundary(self, e : edge) -> None:
		...

	def split(self, e : edge) -> edge:
		"""Splits edge e, updates clustercage lists if necessary and returns new edge."""
		...

	@overload
	def writeGML(self, fileName : str) -> None:
		...

	@overload
	def writeGML(self, fileName : str, drawing : Layout) -> None:
		...

	@overload
	def writeGML(self, os : std.ostream, drawing : Layout) -> None:
		...

	def convertClusterGraph(self, act : cluster, currentEdge : AdjEntryArray[edge], outEdge : AdjEntryArray[  int ]) -> None:
		"""Insert boundaries for all given clusters."""
		...

	def insertBoundary(self, C : cluster, currentEdge : AdjEntryArray[edge], outEdge : AdjEntryArray[  int ], clusterIsLeaf : bool) -> None:
		"""Insert edges to represent the cluster boundary."""
		...

	def reinsertEdge(self, e : edge) -> None:
		"""Reinserts edges to planarize the graph after convertClusterGraph."""
		...
