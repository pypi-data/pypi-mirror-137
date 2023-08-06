# file stubs/ogdf/ClusterGraph.py generated from classogdf_1_1_cluster_graph
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
NODELIST = TypeVar('NODELIST')

CLUSTERLIST = TypeVar('CLUSTERLIST')

ADJLIST = TypeVar('ADJLIST')

LISTITERATOR = TypeVar('LISTITERATOR')

EDGELIST = TypeVar('EDGELIST')

class ClusterGraph(ogdf.GraphObserver):

	"""Representation of clustered graphs."""

	# Iterators

	#: Provides a bidirectional iterator to a cluster in a clustered graph.
	cluster_iterator : Type = internal.GraphIterator[cluster]

	# Graph object containers

	#: The container containing all cluster objects.
	clusters : internal.GraphObjectContainer[ClusterElement] = ...

	@overload
	def __init__(self) -> None:
		"""Creates a cluster graph associated with no graph."""
		...

	@overload
	def __init__(self, G : Graph) -> None:
		"""Creates a cluster graph associated with graphG."""
		...

	@overload
	def __init__(self, C : ClusterGraph) -> None:
		"""Copy constructor."""
		...

	@overload
	def __init__(self, C : ClusterGraph, G : Graph) -> None:
		"""Copies the underlying graph ofCintoGand constructs a copy ofCassociated withG."""
		...

	@overload
	def __init__(self, C : ClusterGraph, G : Graph, originalClusterTable : ClusterArray[cluster], originalNodeTable : NodeArray[node]) -> None:
		"""Copies the underlying graph ofCintoGand constructs a copy ofCassociated withG."""
		...

	@overload
	def __init__(self, C : ClusterGraph, G : Graph, originalClusterTable : ClusterArray[cluster], originalNodeTable : NodeArray[node], edgeCopy : EdgeArray[edge]) -> None:
		"""Copies the underlying graph ofCintoGand constructs a copy ofCassociated withG."""
		...

	def __destruct__(self) -> None:
		"""Destructor."""
		...

	# Access methods

	def rootCluster(self) -> cluster:
		"""Returns the root cluster."""
		...

	def numberOfClusters(self) -> int:
		"""Returns the number of clusters."""
		...

	def maxClusterIndex(self) -> int:
		"""Returns the maximal used cluster index."""
		...

	def clusterArrayTableSize(self) -> int:
		"""Returns the table size of cluster arrays associated with this graph."""
		...

	def clusterOf(self, v : node) -> cluster:
		"""Returns the cluster to which a node belongs."""
		...

	def clusterDepth(self, c : cluster) -> int:
		"""Returns depth of cluster c in cluster tree, starting with root depth 1."""
		...

	def firstCluster(self) -> cluster:
		"""Returns the first cluster in the list of all clusters."""
		...

	def lastCluster(self) -> cluster:
		"""Returns the last cluster in the list of all cluster."""
		...

	def firstPostOrderCluster(self) -> cluster:
		"""Returns the first cluster in the list of post ordered clusters."""
		...

	def allClusters(self, clusterList : CLUSTERLIST) -> None:
		"""Returns the list of all clusters inclusterList."""
		...

	# Modification methods

	def clear(self) -> None:
		"""Removes all clusters except for the root cluster."""
		...

	def init(self, G : Graph) -> None:
		"""Clears all cluster data and then reinitializes the instance with underlying graphG."""
		...

	def clearClusterTree(self, C : cluster) -> None:
		"""Removes all clusters from the cluster subtree rooted at cluster C except for cluster C itself."""
		...

	def newCluster(self, parent : cluster, id : int = -1) -> cluster:
		"""Inserts a new cluster; makes it a child of the clusterparent."""
		...

	def createEmptyCluster(self, parent : cluster = None, clusterId : int = -1) -> cluster:
		"""Creates an empty cluster with indexclusterIdand parentparent."""
		...

	def createCluster(self, nodes : SList[node], parent : cluster = None) -> cluster:
		"""Creates a new cluster containing the nodes given bynodes; makes it a child of the clusterparent."""
		...

	def delCluster(self, c : cluster) -> None:
		"""Deletes clusterc."""
		...

	def moveCluster(self, c : cluster, newParent : cluster) -> None:
		"""Moves clustercto a new parentnewParent."""
		...

	def reassignNode(self, v : node, c : cluster) -> None:
		"""Reassigns nodevto clusterc."""
		...

	@overload
	def reInit(self, G : Graph) -> None:
		"""Clear cluster info structure, reinitializes with underlying graphG."""
		...

	def collapse(self, nodes : NODELIST, G : Graph) -> None:
		"""Collapses all nodes in the listnodesto the first node; multi-edges are removed."""
		...

	# Cluster tree queries

	def setUpdateDepth(self, b : bool) -> None:
		"""Turns automatic update of node depth values on or off."""
		...

	def pullUpSubTree(self, c : cluster) -> None:
		"""Updates depth information in subtree after delCluster."""
		...

	def treeDepth(self) -> int:
		"""Computes depth of cluster tree, running time O(C)."""
		...

	def computeSubTreeDepth(self, c : cluster) -> None:
		"""Computes depth of cluster tree hanging atc."""
		...

	@overload
	def commonCluster(self, nodes : SList[node]) -> cluster:
		"""Returns lowest common cluster of nodes in listnodes."""
		...

	@overload
	def commonCluster(self, v : node, w : node) -> cluster:
		"""Returns the lowest common cluster ofvandwin the cluster tree."""
		...

	def commonClusterLastAncestors(self, v : node, w : node, c1 : cluster, c2 : cluster) -> cluster:
		"""Returns the lowest common cluster lca and the highest ancestors on the path to lca."""
		...

	def commonClusterPath(self, v : node, w : node, eL : List[cluster]) -> cluster:
		"""Returns lca ofvandwand stores corresponding path ineL."""
		...

	def commonClusterAncestorsPath(self, v : node, w : node, c1 : cluster, c2 : cluster, eL : List[cluster]) -> cluster:
		"""Returns lca ofvandw, stores corresponding path ineLand ancestors inc1,c2."""
		...

	def emptyClusters(self, emptyCluster : SList[cluster], checkCluster : SList[cluster] = None) -> None:
		"""Returns the list of clusters that are empty or only contain empty clusters."""
		...

	def emptyOnNodeDelete(self, c : cluster) -> bool:
		"""Returns true if clusterchas only one node and no children."""
		...

	def emptyOnClusterDelete(self, c : cluster) -> bool:
		"""Returns true if clusterchas only one child and no nodes."""
		...

	# Adjacent edges

	def adjEdges(self, c : cluster, edges : EDGELIST) -> None:
		"""Returns the list of all edges adjacent to clustercinedges."""
		...

	def adjEntries(self, c : cluster, entries : ADJLIST) -> None:
		"""Returns the list of all adjacency entries adjacent to clustercinentries."""
		...

	def makeAdjEntries(self, c : cluster, start : LISTITERATOR) -> None:
		"""Computes the adjacency entry list for clusterc."""
		...

	def adjAvailable(self, val : bool) -> None:
		"""Sets the availability status of the adjacency entries."""
		...

	# Miscellaneous

	def representsCombEmbedding(self) -> bool:
		"""Checks the combinatorial cluster planar embedding."""
		...

	# Registering arrays and observers

	def registerArray(self, pClusterArray : ClusterArrayBase) -> ListIterator[ClusterArrayBase]:
		"""Registers a cluster array."""
		...

	def unregisterArray(self, it : ListIterator[ClusterArrayBase]) -> None:
		"""Unregisters a cluster array."""
		...

	def moveRegisterArray(self, it : ListIterator[ClusterArrayBase], pClusterArray : ClusterArrayBase) -> None:
		"""Move the registrationitof a cluster array topClusterArray(used with move semantics for cluster arrays)."""
		...

	def registerObserver(self, pObserver : ClusterGraphObserver) -> ListIterator[ClusterGraphObserver]:
		"""Registers a cluster graph observer."""
		...

	def unregisterObserver(self, it : ListIterator[ClusterGraphObserver]) -> None:
		"""Unregisters a cluster graph observer."""
		...

	# Operators and conversion

	#: Used to save last search run number for commoncluster.
	m_lcaSearch : ClusterArray[  int ] = ...

	#: Used to save last search run number for commoncluster.
	m_lcaNumber : int = ...

	#: Used to save last search run number for commoncluster.
	m_vAncestor : ClusterArray[cluster] = ...

	#: Used to save last search run number for commoncluster.
	m_wAncestor : ClusterArray[cluster] = ...

	#: Depth of clusters is always updated if set to true.
	m_updateDepth : bool = ...

	#: Status of cluster depth information.
	m_depthUpToDate : bool = ...

	def __Graph__(self) -> None:
		"""Conversion to constGraphreference (to underlying graph)."""
		...

	def constGraph(self) -> Graph:
		"""Returns a reference to the underlying graph."""
		...

	def __assign__(self, C : ClusterGraph) -> ClusterGraph:
		"""Assignment operator."""
		...

	@overload
	def doCreateCluster(self, nodes : SList[node], parent : cluster, clusterId : int = -1) -> cluster:
		"""Creates new cluster containing nodes in parameter list with indexclusterId."""
		...

	@overload
	def doCreateCluster(self, nodes : SList[node], emptyCluster : SList[cluster], parent : cluster, clusterId : int = -1) -> cluster:
		"""Creates new cluster containing nodes in parameter list and stores resulting empty clusters in list, cluster has indexclusterId."""
		...

	def doClear(self) -> None:
		"""Clears all cluster data."""
		...

	def copyLCA(self, C : ClusterGraph) -> None:
		"""Copies lowest common ancestor info to copy of clustered graph."""
		...

	def updatePostOrder(self, c : cluster, oldParent : cluster, newParent : cluster) -> None:
		"""Adjusts the post order structure for moved clusters."""
		...

	def postOrderPredecessor(self, c : cluster) -> cluster:
		"""Computes new predecessor for subtree at moved clusterc(nullptr ifcis the root)."""
		...

	def leftMostCluster(self, c : cluster) -> cluster:
		"""Leftmost cluster in subtree rooted at c, gets predecessor of subtree."""
		...

	# Functions inherited from GraphObserver (define how to cope with graph changes)

	def nodeDeleted(self, v : node) -> None:
		"""Implementation of inherited method: Updates data if node deleted."""
		...

	def nodeAdded(self, v : node) -> None:
		"""Implementation of inherited method: Updates data if node added."""
		...

	def edgeDeleted(self, _ : edge) -> None:
		"""Implementation of inherited method: Updates data if edge deleted."""
		...

	def edgeAdded(self, _ : edge) -> None:
		"""Implementation of inherited method: Updates data if edge added."""
		...

	@overload
	def reInit(self) -> None:
		"""Currently does nothing."""
		...

	def cleared(self) -> None:
		"""Clears cluster data without deleting root when underlying graphs' clear method is called."""
		...
