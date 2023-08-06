# file stubs/ogdf/ClusterElement.py generated from classogdf_1_1_cluster_element
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
class ClusterElement(ogdf.internal.GraphElement):

	"""Representation of clusters in a clustered graph."""

	# Graph object containers

	#: The container containing the nodes lying (directly) in this cluster.
	nodes : ListContainer[node,ClusterElement] = ...

	#: The container containing the child clusters (children in the cluster tree) of this cluster.
	children : ListContainer[cluster,ClusterElement] = ...

	#: The container containing the sorted list of adjacency entries of edges leaving this cluster.
	adjEntries : ListContainer[adjEntry,ClusterElement] = ...

	def __init__(self, id : int) -> None:
		"""Creates a new cluster element."""
		...

	# Access methods

	def index(self) -> int:
		"""Returns the (unique) index of the cluster."""
		...

	def depth(self) -> int:
		"""Returns the depth of the cluster in the cluster tree."""
		...

	def parent(self) -> cluster:
		"""Returns the parent of the cluster."""
		...

	def succ(self) -> cluster:
		"""Returns the successor of the cluster in the list of all clusters."""
		...

	def pred(self) -> cluster:
		"""Returns the predecessor of the cluster in the list of all clusters."""
		...

	def pSucc(self) -> cluster:
		"""Returns the postorder successor of the cluster in the list of all clusters."""
		...

	def pPred(self) -> cluster:
		"""Returns the postorder predecessor of the cluster in the list of all clusters."""
		...

	@overload
	def getClusterNodes(self, clusterNodes : List[node]) -> None:
		"""Returns the list of nodes in the cluster, i.e., all nodes in the subtree rooted at this cluster."""
		...

	@overload
	def getClusterNodes(self, clusterNode : NodeArray[ bool ]) -> int:
		"""Sets the entry for each node v to true if v is a member of the subgraph induced by theClusterElement."""
		...

	# Iteration over tree structure

	def cBegin(self) -> ListConstIterator[ClusterElement]:
		"""Returns the first element in the list of child clusters."""
		...

	def crBegin(self) -> ListConstIterator[ClusterElement]:
		"""Returns the last element in the list of child clusters."""
		...

	def cCount(self) -> int:
		"""Returns the number of child clusters."""
		...

	def nBegin(self) -> ListConstIterator[node]:
		"""Returns the first element in list of child nodes."""
		...

	def nCount(self) -> int:
		"""Returns the number of child nodes."""
		...

	def firstAdj(self) -> ListConstIterator[adjEntry]:
		"""Returns the first adjacency entry in the list of outgoing edges."""
		...

	def lastAdj(self) -> ListConstIterator[adjEntry]:
		"""Returns the last adjacency entry in the list of outgoing edges."""
		...

	def compare(self, x : ClusterElement, y : ClusterElement) -> int:
		"""Standard Comparer (uses cluster indices)."""
		...
