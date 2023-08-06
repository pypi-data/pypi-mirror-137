# file stubs/ogdf/__init__.py generated from namespaceogdf
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
E1 = TypeVar('E1')

LISTITERATOR = TypeVar('LISTITERATOR')

Impl = TypeVar('Impl')

COMPARER = TypeVar('COMPARER')

TPath = TypeVar('TPath')

EDGELIST = TypeVar('EDGELIST')

INFO = TypeVar('INFO')

TYPE = TypeVar('TYPE')

FromClass = TypeVar('FromClass')

INDEX = TypeVar('INDEX')

NODELIST = TypeVar('NODELIST')

CONTAINER = TypeVar('CONTAINER')

LIST = TypeVar('LIST')

CMP = TypeVar('CMP')

TCost = TypeVar('TCost')

ONLY_ONCE = TypeVar('ONLY_ONCE')

E = TypeVar('E')

PointType = TypeVar('PointType')

C = TypeVar('C')

NODELISTITERATOR = TypeVar('NODELISTITERATOR')

ToClass = TypeVar('ToClass')

T = TypeVar('T')

TEdges = TypeVar('TEdges')

E2 = TypeVar('E2')

D = TypeVar('D')

P = TypeVar('P')

KEY = TypeVar('KEY')

class ogdf(object):

	"""The namespace for all OGDF objects."""

	# Methods for induced subgraphs

	@overload
	def inducedSubGraph(self, G : Graph, start : LISTITERATOR, subGraph : Graph) -> None:
		"""Computes the subgraph induced by a list of nodes."""
		...

	@overload
	def inducedSubGraph(self, G : Graph, start : LISTITERATOR, subGraph : Graph, nodeTableOrig2New : NodeArray[node]) -> None:
		"""Computes the subgraph induced by a list of nodes (plus a mapping from original nodes to new copies)."""
		...

	@overload
	def inducedSubGraph(self, G : Graph, start : LISTITERATOR, subGraph : Graph, nodeTableOrig2New : NodeArray[node], edgeTableOrig2New : EdgeArray[edge]) -> None:
		"""Computes the subgraph induced by a list of nodes (plus mappings from original nodes and edges to new copies)."""
		...

	def inducedSubgraph(self, G : Graph, it : NODELISTITERATOR, E : EDGELIST) -> None:
		"""Computes the edges in a node-induced subgraph."""
		...

	# Methods for clustered graphs

	def isCConnected(self, C : ClusterGraph) -> bool:
		"""Returns true iff cluster graphCis c-connected."""
		...

	def makeCConnected(self, C : ClusterGraph, G : Graph, addedEdges : List[edge], simple : bool = True) -> None:
		"""Makes a cluster graph c-connected by adding edges."""
		...

	# Methods for minimum spanning tree computation

	@overload
	def computeMinST(self, G : Graph, weight : EdgeArray[ T ], isInTree : EdgeArray[ bool ]) -> T:
		"""Computes a minimum spanning tree using Prim's algorithm."""
		...

	@overload
	def computeMinST(self, G : Graph, weight : EdgeArray[ T ], pred : NodeArray[edge], isInTree : EdgeArray[ bool ]) -> T:
		"""Computes a minimum spanning tree (MST) using Prim's algorithm."""
		...

	@overload
	def computeMinST(self, G : Graph, weight : EdgeArray[ T ], pred : NodeArray[edge]) -> None:
		"""Computes a minimum spanning tree (MST) using Prim's algorithm."""
		...

	@overload
	def computeMinST(self, s : node, G : Graph, weight : EdgeArray[ T ], pred : NodeArray[edge]) -> None:
		"""Computes a minimum spanning tree (MST) using Prim's algorithm."""
		...

	@overload
	def computeMinST(self, s : node, G : Graph, weight : EdgeArray[ T ], pred : NodeArray[edge], isInTree : EdgeArray[ bool ]) -> T:
		"""Computes a minimum spanning tree (MST) using Prim's algorithm."""
		...

	def makeMinimumSpanningTree(self, G : Graph, weight : EdgeArray[ T ]) -> T:
		"""Reduce a graph to its minimum spanning tree (MST) using Kruskal's algorithm."""
		...

	# Deterministic graph generators

	@overload
	def customGraph(self, G : Graph, n : int, edges : List[ std.pair[  int,  int ]], nodes : Array[node]) -> None:
		"""Creates a custom graph using a list of pairs to determine the graph's edges."""
		...

	@overload
	def customGraph(self, G : Graph, n : int, edges : List[ std.pair[  int,  int ]]) -> None:
		"""Creates a custom graph using a list of pairs to determine the graph's edges."""
		...

	def circulantGraph(self, G : Graph, n : int, jumps : Array[  int ]) -> None:
		"""Creates a circulant graph."""
		...

	def regularLatticeGraph(self, G : Graph, n : int, k : int) -> None:
		"""Creates a regular lattice graph."""
		...

	def regularTree(self, G : Graph, n : int, children : int) -> None:
		"""Creates a regular tree."""
		...

	def completeGraph(self, G : Graph, n : int) -> None:
		"""Creates the complete graphK_n."""
		...

	def completeKPartiteGraph(self, G : Graph, signature : Array[  int ]) -> None:
		"""Creates the complete k-partite graphK_{k1,k2,...,kn}."""
		...

	def completeBipartiteGraph(self, G : Graph, n : int, m : int) -> None:
		"""Creates the complete bipartite graphK_{n,m}."""
		...

	def wheelGraph(self, G : Graph, n : int) -> None:
		"""Creates the graphW_n:A wheel graph."""
		...

	def cubeGraph(self, G : Graph, n : int) -> None:
		"""Creates the graphQ^n: An-cube graph."""
		...

	def suspension(self, G : Graph, s : int) -> None:
		"""ModifiesGby adding itss-th suspension."""
		...

	def gridGraph(self, G : Graph, n : int, m : int, loopN : bool, loopM : bool) -> None:
		"""Creates a (toroidal) grid graph onnxmnodes."""
		...

	def petersenGraph(self, G : Graph, n : int = 5, m : int = 2) -> None:
		"""Creates a generalized Petersen graph."""
		...

	def emptyGraph(self, G : Graph, nodes : int) -> None:
		"""Creates a graph withnodesnodes and no edges."""
		...

	# Graph operations

	NodeMap : Type = NodeArray[NodeArray[node] ]

	@overload
	def graphUnion(self, G1 : Graph, G2 : Graph) -> None:
		"""Forms the disjoint union ofG1andG2."""
		...

	@overload
	def graphUnion(self, G1 : Graph, G2 : Graph, map2to1 : NodeArray[node], parallelfree : bool = False, directed : bool = False) -> None:
		"""Forms the union ofG1andG2while identifying nodes fromG2with nodes fromG1."""
		...

	def graphProduct(self, G1 : Graph, G2 : Graph, product : Graph, nodeInProduct : NodeMap, addEdges : Callable) -> None:
		"""Computes the graph product ofG1andG2, using a given function to add edges."""
		...

	def cartesianProduct(self, G1 : Graph, G2 : Graph, product : Graph, nodeInProduct : NodeMap) -> None:
		"""Computes the Cartesian product ofG1andG2and assigns it toproduct, with$E = \{(\langle v_1,w_1\rangle, \langle v_1,w_2\rangle) | (w_1,w_2) \in E_2\} \cup \{(\langle v_1,w_1\rangle, \langle v_2,w_1\rangle) | (v_1,v_2) \in E_1\} $."""
		...

	def tensorProduct(self, G1 : Graph, G2 : Graph, product : Graph, nodeInProduct : NodeMap) -> None:
		"""Computes the tensor product ofG1andG2and assigns it toproduct, with$E = \{(\langle v_1,w_1\rangle, \langle v_2,w_2\rangle) | (v_1,v_2) \in E_1 \land (w_1,w_2) \in E_2\} $."""
		...

	def lexicographicalProduct(self, G1 : Graph, G2 : Graph, product : Graph, nodeInProduct : NodeMap) -> None:
		"""Computes the lexicographical product ofG1andG2and assigns it toproduct, with$E = \{(\langle v_1,w_1\rangle, \langle v_2,w_2\rangle) | (v_1,v_2) \in E_1\} \cup \{(\langle v_1,w_1\rangle, \langle v_1,w_2\rangle) | (w_1,w_2) \in E_2\} $."""
		...

	def strongProduct(self, G1 : Graph, G2 : Graph, product : Graph, nodeInProduct : NodeMap) -> None:
		"""Computes the strong product ofG1andG2and assigns it toproduct, with$E = \{(\langle v_1,w_1\rangle, \langle v_1,w_2\rangle) | (w_1,w_2) \in E_2\} \cup \{(\langle v_1,w_1\rangle, \langle v_2,w_1\rangle) | (v_1,v_2) \in E_1\} \cup \{(\langle v_1,w_1\rangle, \langle v_2,w_2\rangle) | (v_1,v_2) \in E_1 \land (w_1,w_2) \in E_2\} $."""
		...

	def coNormalProduct(self, G1 : Graph, G2 : Graph, product : Graph, nodeInProduct : NodeMap) -> None:
		"""Computes the co-normal product ofG1andG2and assigns it toproduct, with$E = \{(\langle v_1,w_1\rangle, \langle v_2,w_2\rangle) | (v_1,v_2) \in E_1 \lor (w_1,w_2) \in E_2\} $."""
		...

	def modularProduct(self, G1 : Graph, G2 : Graph, product : Graph, nodeInProduct : NodeMap) -> None:
		"""Computes the modular product ofG1andG2and assigns it toproduct, with$E = \{(\langle v_1,w_1\rangle, \langle v_2,w_2\rangle) | (v_1,v_2) \in E_1 \land (w_1,w_2) \in E_2\} \cup \{(\langle v_1,w_1\rangle, \langle v_2,w_2\rangle) | (v_1,v_2) \not\in E_1 \land (w_1,w_2) \not\in E_2\} $."""
		...

	def rootedProduct(self, G1 : Graph, G2 : Graph, product : Graph, nodeInProduct : NodeMap, rootInG2 : node) -> None:
		"""Computes the rooted product ofG1andG2, rooted inrootInG2, and assigns it toproduct."""
		...

	# Randomized graph generators

	@overload
	def randomGeographicalThresholdGraph(self, G : Graph, weights : Array[  int ], dist : D, threshold : float, h : Callable, dimension : int = 2) -> None:
		"""Creates a random geometric graph where edges are created based on their distance and the weight of nodes."""
		...

	@overload
	def randomGeographicalThresholdGraph(self, G : Graph, weights : Array[  int ], dist : D, threshold : float, alpha : int = 2, dimension : int = 2) -> None:
		"""Creates a random geometric graph where edges are created based on their distance and the weight of nodes."""
		...

	def randomHierarchy(self, G : Graph, n : int, m : int, planar : bool, singleSource : bool, longEdges : bool) -> None:
		"""Creates a random hierarchical graph."""
		...

	def randomRegularGraph(self, G : Graph, n : int, d : int) -> None:
		"""Creates a randomd-regular graph."""
		...

	def randomGraph(self, G : Graph, n : int, m : int) -> None:
		"""Creates a random graph."""
		...

	def randomSimpleGraph(self, G : Graph, n : int, m : int) -> bool:
		"""Creates a random simple graph."""
		...

	def randomSimpleGraphByProbability(self, G : Graph, n : int, pEdge : float) -> bool:
		"""Creates a random simple graph."""
		...

	def randomSimpleConnectedGraph(self, G : Graph, n : int, m : int) -> bool:
		"""Creates a random simple and connected graph."""
		...

	def randomBiconnectedGraph(self, G : Graph, n : int, m : int) -> None:
		"""Creates a random biconnected graph."""
		...

	def randomPlanarConnectedGraph(self, G : Graph, n : int, m : int) -> None:
		"""Creates a random connected (simple) planar (embedded) graph."""
		...

	def randomPlanarBiconnectedGraph(self, G : Graph, n : int, m : int, multiEdges : bool = False) -> None:
		"""Creates a random planar biconnected (embedded) graph."""
		...

	def randomPlanarBiconnectedDigraph(self, G : Graph, n : int, m : int, p : float = 0, multiEdges : bool = False) -> None:
		"""Creates a random planar biconnected acyclic (embedded) digraph."""
		...

	def randomUpwardPlanarBiconnectedDigraph(self, G : Graph, n : int, m : int) -> None:
		"""Creates a random upward planar biconnected (embedded) digraph."""
		...

	def randomPlanarCNBGraph(self, G : Graph, n : int, m : int, b : int) -> None:
		"""Creates a random planar graph, that is connected, but not biconnected."""
		...

	def randomTriconnectedGraph(self, G : Graph, n : int, p1 : float, p2 : float) -> None:
		"""Creates a random triconnected (and simple) graph."""
		...

	@overload
	def randomPlanarTriconnectedGraph(self, G : Graph, n : int, m : int) -> None:
		"""Creates a random planar triconnected (and simple) graph."""
		...

	@overload
	def randomPlanarTriconnectedGraph(self, G : Graph, n : int, p1 : float, p2 : float) -> None:
		"""Creates a random planar triconnected (and simple) graph."""
		...

	@overload
	def randomTree(self, G : Graph, n : int) -> None:
		"""Creates a random tree (simpler version."""
		...

	@overload
	def randomTree(self, G : Graph, n : int, maxDeg : int, maxWidth : int) -> None:
		"""Creates a random tree."""
		...

	def randomClusterPlanarGraph(self, C : ClusterGraph, G : Graph, cNum : int) -> None:
		"""Assigns random clusters to a given graphG."""
		...

	@overload
	def randomClusterGraph(self, C : ClusterGraph, G : Graph, cNum : int) -> None:
		"""Assigns random clusters to a given graphG."""
		...

	@overload
	def randomClusterGraph(self, C : ClusterGraph, G : Graph, root : node, moreInLeaves : int) -> None:
		"""Assigns a specified cluster structure to a given graphG, and assigns vertices to clusters."""
		...

	def randomDigraph(self, G : Graph, n : int, p : float) -> None:
		"""Creates a random (simple) directed graph."""
		...

	def randomSeriesParallelDAG(self, G : Graph, edges : int, p : float = 0.5, flt : float = 0.0) -> None:
		"""Creates a random (simple, biconnected) series parallel DAG."""
		...

	def randomGeometricCubeGraph(self, G : Graph, nodes : int, threshold : float, dimension : int = 2) -> None:
		"""Creates a random geometric graph by laying out nodes in a unit n-cube. Nodes with a distance < threshold are connected, 0 <= threshold <= sqrt(dimension). The graph is simple."""
		...

	def randomWaxmanGraph(self, G : Graph, nodes : int, alpha : float, beta : float, width : float = 1.0, height : float = 1.0) -> None:
		"""Generates a Waxman graph where nodes are uniformly randomly placed in a grid, then edges are inserted based on nodes' euclidean distances."""
		...

	def preferentialAttachmentGraph(self, G : Graph, nodes : int, minDegree : int) -> None:
		"""Creates a graph where new nodes are more likely to connect to nodes with high degree."""
		...

	def randomWattsStrogatzGraph(self, G : Graph, n : int, k : int, probability : float) -> None:
		"""Creates a "small world" graph as described by Watts & Strogatz."""
		...

	def randomChungLuGraph(self, G : Graph, expectedDegreeDistribution : Array[  int ]) -> None:
		"""Creates a graph where edges are inserted based on given weights."""
		...

	def randomEdgesGraph(self, G : Graph, probability : Callable) -> None:
		"""Inserts edges into the given graph based on probabilities given by a callback function."""
		...

	# Methods for loops

	def removeSelfLoops(self, graph : Graph, v : node) -> None:
		"""Removes all self-loops for a given nodevingraph."""
		...

	def isLoopFree(self, G : Graph) -> bool:
		"""Returns true iffGcontains no self-loop."""
		...

	@overload
	def makeLoopFree(self, G : Graph, L : NODELIST) -> None:
		"""Removes all self-loops fromGand returns all nodes with self-loops inL."""
		...

	def hasNonSelfLoopEdges(self, G : Graph) -> bool:
		"""Returns whetherGhas edges which are not self-loops."""
		...

	@overload
	def makeLoopFree(self, G : Graph) -> None:
		"""Removes all self-loops fromG."""
		...

	# Methods for parallel edges

	def parallelFreeSort(self, G : Graph, edges : SListPure[edge]) -> None:
		"""Sorts the edges ofGsuch that parallel edges come after each other in the list."""
		...

	def isParallelFree(self, G : Graph) -> bool:
		"""Returns true iffGcontains no parallel edges."""
		...

	def numParallelEdges(self, G : Graph) -> int:
		"""Returns the number of parallel edges inG."""
		...

	@overload
	def makeParallelFree(self, G : Graph, parallelEdges : EDGELIST) -> None:
		"""Removes all but one of each bundle of parallel edges."""
		...

	@overload
	def makeParallelFree(self, G : Graph) -> None:
		"""Removes all but one edge of each bundle of parallel edges inG."""
		...

	def parallelFreeSortUndirected(self, G : Graph, edges : SListPure[edge], minIndex : EdgeArray[  int ], maxIndex : EdgeArray[  int ]) -> None:
		"""Sorts the edges ofGsuch that undirected parallel edges come after each other in the list."""
		...

	def isParallelFreeUndirected(self, G : Graph) -> bool:
		"""Returns true iffGcontains no undirected parallel edges."""
		...

	def numParallelEdgesUndirected(self, G : Graph) -> int:
		"""Returns the number of undirected parallel edges inG."""
		...

	def getParallelFreeUndirected(self, G : Graph, parallelEdges : EdgeArray[ EDGELIST ]) -> None:
		"""Computes the bundles of undirected parallel edges inG."""
		...

	@overload
	def makeParallelFreeUndirected(self, G : Graph, parallelEdges : EDGELIST = None, cardPositive : EdgeArray[  int ] = None, cardNegative : EdgeArray[  int ] = None) -> None:
		"""Removes all but one edge of each bundle of undirected parallel edges."""
		...

	@overload
	def makeParallelFreeUndirected(self, G : Graph, parallelEdges : EDGELIST) -> None:
		...

	@overload
	def makeParallelFreeUndirected(self, G : Graph, parallelEdges : EDGELIST, cardPositive : EdgeArray[  int ], cardNegative : EdgeArray[  int ]) -> None:
		...

	# Methods for simple graphs

	def isSimple(self, G : Graph) -> bool:
		"""Returns true iffGcontains neither self-loops nor parallel edges."""
		...

	def makeSimple(self, G : Graph) -> None:
		"""Removes all self-loops and all but one edge of each bundle of parallel edges."""
		...

	def isSimpleUndirected(self, G : Graph) -> bool:
		"""Returns true iffGcontains neither self-loops nor undirected parallel edges."""
		...

	def makeSimpleUndirected(self, G : Graph) -> None:
		"""Removes all self-loops and all but one edge of each bundle of undirected parallel edges."""
		...

	# Methods for connectivity

	def isConnected(self, G : Graph) -> bool:
		"""Returns true iffGis connected."""
		...

	@overload
	def makeConnected(self, G : Graph, added : List[edge]) -> None:
		"""MakesGconnected by adding a minimum number of edges."""
		...

	@overload
	def makeConnected(self, G : Graph) -> None:
		"""makesGconnected by adding a minimum number of edges."""
		...

	def connectedComponents(self, G : Graph, component : NodeArray[  int ], isolated : List[node] = None) -> int:
		"""Computes the connected components ofGand optionally generates a list of isolated nodes."""
		...

	def connectedIsolatedComponents(self, G : Graph, isolated : List[node], component : NodeArray[  int ]) -> int:
		"""Computes the connected components ofGand optionally generates a list of isolated nodes."""
		...

	@overload
	def isBiconnected(self, G : Graph, cutVertex : node) -> bool:
		"""Returns true iffGis biconnected."""
		...

	@overload
	def isBiconnected(self, G : Graph) -> bool:
		"""Returns true iffGis biconnected."""
		...

	@overload
	def makeBiconnected(self, G : Graph, added : List[edge]) -> None:
		"""MakesGbiconnected by adding edges."""
		...

	@overload
	def makeBiconnected(self, G : Graph) -> None:
		"""MakesGbiconnected by adding edges."""
		...

	@overload
	def biconnectedComponents(self, G : Graph, component : EdgeArray[  int ], nonEmptyComponents : int) -> int:
		"""Computes the biconnected components ofG."""
		...

	@overload
	def biconnectedComponents(self, G : Graph, component : EdgeArray[  int ]) -> int:
		"""Computes the biconnected components ofG."""
		...

	@overload
	def isTwoEdgeConnected(self, graph : Graph, bridge : edge) -> bool:
		"""Returns true iffgraphis 2-edge-connected."""
		...

	@overload
	def isTwoEdgeConnected(self, graph : Graph) -> bool:
		"""Returns true iffgraphis 2-edge-connected."""
		...

	@overload
	def isTriconnected(self, G : Graph, s1 : node, s2 : node) -> bool:
		"""Returns true iffGis triconnected."""
		...

	@overload
	def isTriconnected(self, G : Graph) -> bool:
		"""Returns true iffGis triconnected."""
		...

	@overload
	def isTriconnectedPrimitive(self, G : Graph, s1 : node, s2 : node) -> bool:
		"""Returns true iffGis triconnected (using a quadratic time algorithm!)."""
		...

	@overload
	def isTriconnectedPrimitive(self, G : Graph) -> bool:
		"""Returns true iffGis triconnected (using a quadratic time algorithm!)."""
		...

	def triangulate(self, G : Graph) -> None:
		"""Triangulates a planarly embedded graphGby adding edges."""
		...

	# Methods for directed graphs

	@overload
	def isAcyclic(self, G : Graph, backedges : List[edge]) -> bool:
		"""Returns true iff the digraphGis acyclic."""
		...

	@overload
	def isAcyclic(self, G : Graph) -> bool:
		"""Returns true iff the digraphGis acyclic."""
		...

	@overload
	def isAcyclicUndirected(self, G : Graph, backedges : List[edge]) -> bool:
		"""Returns true iff the undirected graphGis acyclic."""
		...

	@overload
	def isAcyclicUndirected(self, G : Graph) -> bool:
		"""Returns true iff the undirected graphGis acyclic."""
		...

	def makeAcyclic(self, G : Graph) -> None:
		"""Makes the digraphGacyclic by removing edges."""
		...

	def makeAcyclicByReverse(self, G : Graph) -> None:
		"""Makes the digraph G acyclic by reversing edges."""
		...

	@overload
	def hasSingleSource(self, G : Graph, source : node) -> bool:
		"""Returns true iff the digraphGcontains exactly one source node (or is empty)."""
		...

	@overload
	def hasSingleSource(self, G : Graph) -> bool:
		"""Returns true iff the digraphGcontains exactly one source node (or is empty)."""
		...

	@overload
	def hasSingleSink(self, G : Graph, sink : node) -> bool:
		"""Returns true iff the digraphGcontains exactly one sink node (or is empty)."""
		...

	@overload
	def hasSingleSink(self, G : Graph) -> bool:
		"""Returns true iff the digraphGcontains exactly one sink node (or is empty)."""
		...

	@overload
	def isStGraph(self, G : Graph, s : node, t : node, st : edge) -> bool:
		"""Returns true iffGis an st-digraph."""
		...

	@overload
	def isStGraph(self, G : Graph) -> bool:
		"""Returns true ifGis an st-digraph."""
		...

	def topologicalNumbering(self, G : Graph, num : NodeArray[  int ]) -> None:
		"""Computes a topological numbering of an acyclic digraphG."""
		...

	def strongComponents(self, G : Graph, component : NodeArray[  int ]) -> int:
		"""Computes the strongly connected components of the digraphG."""
		...

	@overload
	def makeBimodal(self, G : Graph, newEdges : List[edge]) -> None:
		"""Makes the digraphGbimodal."""
		...

	@overload
	def makeBimodal(self, G : Graph) -> None:
		"""Makes the digraphGbimodal."""
		...

	# Methods for trees and forests

	def isFreeForest(self, G : Graph) -> bool:
		"""Returns true iff the undirected graphGis acyclic."""
		...

	def isTree(self, G : Graph) -> bool:
		"""Returns true iffGis a tree, i.e. contains no undirected cycle and is connected."""
		...

	@overload
	def isArborescenceForest(self, G : Graph, roots : List[node]) -> bool:
		"""Returns true iffGis a forest consisting only of arborescences."""
		...

	@overload
	def isArborescenceForest(self, G : Graph) -> bool:
		"""Returns true iffGis a forest consisting only of arborescences."""
		...

	@overload
	def isForest(self, G : Graph, roots : List[node]) -> bool:
		"""Returns true iffGis a forest consisting only of arborescences."""
		...

	@overload
	def isForest(self, G : Graph) -> bool:
		"""Returns true iffGis a forest consisting only of arborescences."""
		...

	@overload
	def isArborescence(self, G : Graph, root : node) -> bool:
		"""Returns true iffGrepresents an arborescence."""
		...

	@overload
	def isArborescence(self, G : Graph) -> bool:
		"""Returns true iffGrepresents an arborescence."""
		...

	# Iteration macros

	def test_forall_adj_entries_of_cluster(self, it : ListConstIterator[adjEntry], adj : adjEntry) -> bool:
		...

	@overload
	def test_forall_adj_edges_of_cluster(self, it : ListConstIterator[adjEntry], e : edge) -> bool:
		...

	@overload
	def test_forall_adj_edges_of_cluster(self, adj : adjEntry, e : edge) -> bool:
		...

	class AlgorithmFailureCode(enum.Enum):

		"""Code for an internal failure condition."""

		Unknown = enum.auto()

		#: function parameter is illegal
		IllegalParameter = enum.auto()

		#: min-cost flow could not find a legal flow
		NoFlow = enum.auto()

		#: sequence not sorted
		Sort = enum.auto()

		#: labelling failed
		Label = enum.auto()

		#: external face not correct
		ExternalFace = enum.auto()

		#: crossing forbidden but necessary
		ForbiddenCrossing = enum.auto()

		#: it took too long
		TimelimitExceeded = enum.auto()

		#: couldn't solve the problem
		NoSolutionFound = enum.auto()

		#: index out of bounds
		IndexOutOfBounds = enum.auto()

		PrimalBound = enum.auto()

		DualBound = enum.auto()

		NotInteger = enum.auto()

		Buffer = enum.auto()

		AddVar = enum.auto()

		Sorter = enum.auto()

		Phase = enum.auto()

		Active = enum.auto()

		NoSolution = enum.auto()

		MakeFeasible = enum.auto()

		Guarantee = enum.auto()

		BranchingVariable = enum.auto()

		Strategy = enum.auto()

		CloseHalf = enum.auto()

		StandardPool = enum.auto()

		Variable = enum.auto()

		LpIf = enum.auto()

		Lp = enum.auto()

		Bstack = enum.auto()

		LpStatus = enum.auto()

		BranchingRule = enum.auto()

		FixSet = enum.auto()

		LpSub = enum.auto()

		String = enum.auto()

		Constraint = enum.auto()

		Pool = enum.auto()

		Global = enum.auto()

		FsVarStat = enum.auto()

		LpVarStat = enum.auto()

		OsiIf = enum.auto()

		ConBranchRule = enum.auto()

		Timer = enum.auto()

		Array = enum.auto()

		Csense = enum.auto()

		BPrioQueue = enum.auto()

		FixCand = enum.auto()

		BHeap = enum.auto()

		Poolslot = enum.auto()

		SparVec = enum.auto()

		Convar = enum.auto()

		Ostream = enum.auto()

		Hash = enum.auto()

		Paramaster = enum.auto()

		InfeasCon = enum.auto()

		STOP = enum.auto()

	class BoyerMyrvoldEdgeType(enum.Enum):

		"""Type of edge."""

		#: undefined
		Undefined = enum.auto()

		#: selfloop
		Selfloop = enum.auto()

		#: backedge
		Back = enum.auto()

		#: DFS-edge.
		Dfs = enum.auto()

		#: parallel DFS-edge
		DfsParallel = enum.auto()

		#: deleted backedge
		BackDeleted = enum.auto()

	class CompressionOptions(enum.Enum):

		"""Defines options for compression search paths."""

		#: Path Compression.
		PathCompression = enum.auto()

		#: Path Splitting (default)
		PathSplitting = enum.auto()

		#: Path Halving.
		PathHalving = enum.auto()

		#: Reversal of type 1.
		Type1Reversal = enum.auto()

		#: Collapsing.
		Collapsing = enum.auto()

		#: No Compression.
		Disabled = enum.auto()

	class ConstraintEdgeType(enum.Enum):

		"""Types of edges in the constraint graph."""

		BasicArc = enum.auto()

		VertexSizeArc = enum.auto()

		VisibilityArc = enum.auto()

		#: can be compacted to zero length, can be fixed
		FixToZeroArc = enum.auto()

		#: can be compacted to zero length
		ReducibleArc = enum.auto()

		#: inserted to replace some reducible in fixzerolength
		MedianArc = enum.auto()

	class CPUFeature(enum.Enum):

		"""Special features supported by a x86/x64 CPU."""

		#: Intel MMX Technology.
		MMX = enum.auto()

		#: Streaming SIMD Extensions (SSE)
		SSE = enum.auto()

		#: Streaming SIMD Extensions 2 (SSE2)
		SSE2 = enum.auto()

		#: Streaming SIMD Extensions 3 (SSE3)
		SSE3 = enum.auto()

		#: Supplemental Streaming SIMD Extensions 3 (SSSE3)
		SSSE3 = enum.auto()

		#: Streaming SIMD Extensions 4.1 (SSE4.1)
		SSE4_1 = enum.auto()

		#: Streaming SIMD Extensions 4.2 (SSE4.2)
		SSE4_2 = enum.auto()

		#: Virtual Machine Extensions.
		VMX = enum.auto()

		#: Safer Mode Extensions.
		SMX = enum.auto()

		#: Enhanced Intel SpeedStep Technology.
		EST = enum.auto()

		#: Processor supports MONITOR/MWAIT instructions.
		MONITOR = enum.auto()

	class CPUFeatureMask(enum.Enum):

		"""Bit mask for CPU features."""

		#: Intel MMX Technology.
		MMX = enum.auto()

		#: Streaming SIMD Extensions (SSE)
		SSE = enum.auto()

		#: Streaming SIMD Extensions 2 (SSE2)
		SSE2 = enum.auto()

		#: Streaming SIMD Extensions 3 (SSE3)
		SSE3 = enum.auto()

		#: Supplemental Streaming SIMD Extensions 3 (SSSE3)
		SSSE3 = enum.auto()

		#: Streaming SIMD Extensions 4.1 (SSE4.1)
		SSE4_1 = enum.auto()

		#: Streaming SIMD Extensions 4.2 (SSE4.2)
		SSE4_2 = enum.auto()

		#: Virtual Machine Extensions.
		VMX = enum.auto()

		#: Safer Mode Extensions.
		SMX = enum.auto()

		#: Enhanced Intel SpeedStep Technology.
		EST = enum.auto()

		#: Processor supports MONITOR/MWAIT instructions.
		MONITOR = enum.auto()

	class Direction(enum.Enum):

		before = enum.auto()

		after = enum.auto()

	class EdgeArrow(enum.Enum):

		"""Types for edge arrows."""

		#: no edge arrows
		_None = enum.auto()

		#: edge arrow at target node of the edge
		Last = enum.auto()

		#: edge arrow at source node of the edge
		First = enum.auto()

		#: edge arrow at target and source node of the edge
		Both = enum.auto()

		Undefined = enum.auto()

	class EdgeStandardType(enum.Enum):

		"""Enumeration class of possible edge standard representations."""

		#: no new dummy nodes are introduced, for every hyperedgee= (v_1, ...,v_l), we add a cliqieK_lconnecting hypernodes incident withe
		clique = enum.auto()

		#: for every hyperedgee= {v_1, ...,v_l}a single new dummy nodev_eis introduced, moreover,v_ebecomes the center of a new star connecting all hypernodes incident with e (ie. {v_1,v_e}, ..., {v_l,v_e}are added)
		star = enum.auto()

		#: for every hyperedgeea minimal subcubic tree connecting all hypernodes incident with e together is added with all its nodes and edges, leaves of tree are hypernodes, all non-leaf nodes are newly introduced dummy nodes.
		tree = enum.auto()

	class FillPattern(enum.Enum):

		"""Fillpatterns."""

		_None = enum.auto()

		Solid = enum.auto()

		Dense1 = enum.auto()

		Dense2 = enum.auto()

		Dense3 = enum.auto()

		Dense4 = enum.auto()

		Dense5 = enum.auto()

		Dense6 = enum.auto()

		Dense7 = enum.auto()

		Horizontal = enum.auto()

		Vertical = enum.auto()

		Cross = enum.auto()

		BackwardDiagonal = enum.auto()

		ForwardDiagonal = enum.auto()

		DiagonalCross = enum.auto()

	class InterleavingOptions(enum.Enum):

		"""Defines options for interleaving find/link operations in quickUnion."""

		#: No Interleaving (default)
		Disabled = enum.auto()

		#: Rem's Algorithm (only compatible with LinkOptions::Index)
		Rem = enum.auto()

		#: Tarjan's and van Leeuwen's Algorithm (only compatible withLinkOptions::Rank)
		Tarjan = enum.auto()

		#: Interleaved Reversal of Type 0 (only compatible with LinkOptions::Naive)
		Type0Reversal = enum.auto()

		#: Interleaved Path Splitting Path Compression (only compatible with LinkOptions::Index)
		SplittingCompression = enum.auto()

	class IntersectionType(enum.Enum):

		"""Determines the type of intersection of two geometric objects."""

		#: Two geometric objects do not intersect.
		_None = enum.auto()

		#: Two geometric objects intersect in a single point.
		SinglePoint = enum.auto()

		#: Two geometric objects intersect in infinitely many points.
		Overlapping = enum.auto()

	class LabelType(enum.Enum):

		End1 = enum.auto()

		Mult1 = enum.auto()

		Name = enum.auto()

		End2 = enum.auto()

		Mult2 = enum.auto()

		#: the number of available labels at an edge
		NumLabels = enum.auto()

	class LibraryNotSupportedCode(enum.Enum):

		"""Code for the library which was intended to get used, but its use is not supported."""

		Unknown = enum.auto()

		#: COIN not supported.
		Coin = enum.auto()

		#: ABACUS not supported.
		Abacus = enum.auto()

		#: the used library doesn't support that function
		FunctionNotImplemented = enum.auto()

		MissingCallbackImplementation = enum.auto()

		STOP = enum.auto()

	class LinkOptions(enum.Enum):

		"""Defines options for linking two sets."""

		#: Naive Link.
		Naive = enum.auto()

		#: Link by index (default)
		Index = enum.auto()

		#: Link by size.
		Size = enum.auto()

		#: Link by rank.
		Rank = enum.auto()

	class NetArcType(enum.Enum):

		defaultArc = enum.auto()

		angle = enum.auto()

		backAngle = enum.auto()

		bend = enum.auto()

	class Orientation(enum.Enum):

		"""Determines the orientation in hierarchical layouts."""

		#: Edges are oriented from top to bottom.
		topToBottom = enum.auto()

		#: Edges are oriented from bottom to top.
		bottomToTop = enum.auto()

		#: Edges are oriented from left to right.
		leftToRight = enum.auto()

		#: Edges are oriented from right to left.
		rightToLeft = enum.auto()

	class OrthoBendType(enum.Enum):

		convexBend = enum.auto()

		reflexBend = enum.auto()

	class OrthoDir(enum.Enum):

		North = enum.auto()

		East = enum.auto()

		South = enum.auto()

		West = enum.auto()

		Undefined = enum.auto()

	class RemoveReinsertType(enum.Enum):

		"""The postprocessing method for edge insertion algorithms."""

		#: No postprocessing.
		_None = enum.auto()

		#: Postprocessing only with the edges that have to be inserted.
		Inserted = enum.auto()

		#: Postprocessing with the edges involved in the most crossings.
		MostCrossed = enum.auto()

		#: Postproceesing with all edges.
		All = enum.auto()

		#: Full postprocessing after each edge insertion.
		Incremental = enum.auto()

		#: Postprocessing for (so far) inserted edges after each edge insertion.
		IncInserted = enum.auto()

	class Shape(enum.Enum):

		"""Types for node shapes."""

		#: rectangle
		Rect = enum.auto()

		#: rectangle with rounded corners
		RoundedRect = enum.auto()

		#: ellipse
		Ellipse = enum.auto()

		#: isosceles triangle (base side down)
		Triangle = enum.auto()

		#: pentagon
		Pentagon = enum.auto()

		#: hexagon
		Hexagon = enum.auto()

		#: octagon
		Octagon = enum.auto()

		#: rhomb (=diamond)
		Rhomb = enum.auto()

		#: trapeze (upper side shorter)
		Trapeze = enum.auto()

		#: parallelogram (slanted to the right)
		Parallelogram = enum.auto()

		#: isosceles triangle (base side up)
		InvTriangle = enum.auto()

		#: inverted trapeze (upper side longer)
		InvTrapeze = enum.auto()

		#: inverted parallelogram (slanted to the left)
		InvParallelogram = enum.auto()

		Image = enum.auto()

	class SpringForceModel(enum.Enum):

		"""The force model used for computing forces on nodes."""

		#: the force model proposed by Fruchterman and Reingold.
		FruchtermanReingold = enum.auto()

		FruchtermanReingoldModAttr = enum.auto()

		FruchtermanReingoldModRep = enum.auto()

		#: the force model proposed by Eades for the original spring embedder.
		Eades = enum.auto()

		#: the force model proposed by Hachul (FMMMLayout)
		Hachul = enum.auto()

		#: the force model proposed by Gronemann (FastMultipoleEmbedder).
		Gronemann = enum.auto()

	class StrokeLineCap(enum.Enum):

		"""Line cap types of strokes."""

		Butt = enum.auto()

		Round = enum.auto()

		Square = enum.auto()

	class StrokeLineJoin(enum.Enum):

		"""Line join types of strokes."""

		Miter = enum.auto()

		Round = enum.auto()

		Bevel = enum.auto()

	class StrokeType(enum.Enum):

		"""Line types of strokes."""

		#: no line
		_None = enum.auto()

		#: solid line
		Solid = enum.auto()

		#: dashed line
		Dash = enum.auto()

		#: dotted line
		Dot = enum.auto()

		#: line style "dash dot dash dot ..."
		Dashdot = enum.auto()

		#: line style "dash dot dot dash dot dot ..."
		Dashdotdot = enum.auto()

	class UMLEdgeTypeConstants(enum.Enum):

		PrimAssociation = enum.auto()

		PrimGeneralization = enum.auto()

		PrimDependency = enum.auto()

		SecExpansion = enum.auto()

		SecDissect = enum.auto()

		SecFaceSplitter = enum.auto()

		SecCluster = enum.auto()

		SecClique = enum.auto()

		Merger = enum.auto()

		Vertical = enum.auto()

		Align = enum.auto()

		AssClass = enum.auto()

		Brother = enum.auto()

		HalfBrother = enum.auto()

		Cousin = enum.auto()

		FifthToMerger = enum.auto()

		FifthFromMerger = enum.auto()

	class UMLEdgeTypeOffsets(enum.Enum):

		Primary = enum.auto()

		Secondary = enum.auto()

		Tertiary = enum.auto()

		Fourth = enum.auto()

		Fifth = enum.auto()

		User = enum.auto()

	class UMLEdgeTypePatterns(enum.Enum):

		Primary = enum.auto()

		Secondary = enum.auto()

		Tertiary = enum.auto()

		Fourth = enum.auto()

		User = enum.auto()

		All = enum.auto()

	class UMLNodeTypeConstants(enum.Enum):

		PrimOriginal = enum.auto()

		PrimCopy = enum.auto()

		SecStructural = enum.auto()

		SecNonStructural = enum.auto()

		TerCrossing = enum.auto()

		TerExpander = enum.auto()

		TerHDExpander = enum.auto()

		TerLDExpander = enum.auto()

		FourFlow = enum.auto()

		FourLabel = enum.auto()

		FourType = enum.auto()

		FourCorner = enum.auto()

	class UMLNodeTypeOffsets(enum.Enum):

		Primary = enum.auto()

		Secondary = enum.auto()

		Tertiary = enum.auto()

		Fourth = enum.auto()

		Fifth = enum.auto()

		User = enum.auto()

	class UMLNodeTypePatterns(enum.Enum):

		Primary = enum.auto()

		Secondary = enum.auto()

		Tertiary = enum.auto()

		Fourth = enum.auto()

		User = enum.auto()

		All = enum.auto()

	class UMLOpt(enum.Enum):

		OpAlign = enum.auto()

		OpScale = enum.auto()

		OpProg = enum.auto()

	class UsedLabels(enum.Enum):

		End1 = enum.auto()

		Mult1 = enum.auto()

		Name = enum.auto()

		End2 = enum.auto()

		Mult2 = enum.auto()

		lAll = enum.auto()

	class whaType(enum.Enum):

		"""The definitions for W, B, H and A describe the type of a node during the computation of the maximal pertinent sequence."""

		W = enum.auto()

		B = enum.auto()

		H = enum.auto()

		A = enum.auto()

	#: The type of adjacency entries.
	adjEntry : Type = AdjElement

	#: The type of adjacency entries.
	adjHypergraphEntry : Type = AdjHypergraphElement

	ArrayConstIterator : Type = E

	ArrayConstReverseIterator : Type = ArrayReverseIteratorBase[ E, True ]

	ArrayIterator : Type = E

	ArrayReverseIterator : Type = ArrayReverseIteratorBase[ E, False ]

	bEdge : Type = BEdge

	#: The type of clusters.
	cluster : Type = ClusterElement

	#: Lines with real coordinates.
	DLine : Type = GenericLine[DPoint]

	#: Representing two-dimensional point with real coordinates.
	DPoint : Type = GenericPoint[ float ]

	#: Polylines with DPoint points.
	DPolyline : Type = GenericPolyline[DPoint]

	#: Segments with real coordinates.
	DSegment : Type = GenericSegment[DPoint]

	#: The type of edges.
	edge : Type = EdgeElement

	edgeType : Type = int

	face : Type = FaceElement

	#: The type of hyperedges.
	hyperedge : Type = HyperedgeElement

	#: The type of hypernodes.
	hypernode : Type = HypernodeElement

	#: Representing a two-dimensional point with integer coordinates.
	IPoint : Type = GenericPoint[  int ]

	#: Polylines with IPoint points.
	IPolyline : Type = GenericPolyline[IPoint]

	ListConstIterator : Type = ListIteratorBase[ E,
	                    True, False ]

	ListConstReverseIterator : Type = ListIteratorBase[ E,
	                    True, True ]

	ListIterator : Type = ListIteratorBase[ E,
	                    False, False ]

	ListReverseIterator : Type = ListIteratorBase[ E,
	                    False, True ]

	#: The type of nodes.
	node : Type = NodeElement

	nodeType : Type = int

	pa_label : Type = PALabel

	#: Prioritizedqueue interface wrapper for heaps.
	PrioritizedQueue : Type = pq_internal.PrioritizedQueue[ E, P, C, Impl ]

	PtrSuperCluster : Type = SuperCluster

	SListConstIterator : Type = SListIteratorBase[ E,
	                    True ]

	SListIterator : Type = SListIteratorBase[ E,
	                    False ]

	SortedSequenceConstIterator : Type = SortedSequenceIteratorBase[ KEY, INFO, CMP, True, False ]

	SortedSequenceConstReverseIterator : Type = SortedSequenceIteratorBase[ KEY, INFO, CMP, True, True ]

	SortedSequenceIterator : Type = SortedSequenceIteratorBase[ KEY, INFO, CMP, False, False ]

	SortedSequenceReverseIterator : Type = SortedSequenceIteratorBase[ KEY, INFO, CMP, False, True ]

	XSequence : Type = SortedSequence[DPointHandle,SeqItemY,EventCmp]

	YSequence : Type = SortedSequence[DSegmentHandle,SeqItemXY,SweepCmp]

	arrow_str : str = ...

	c_maxLengthPerLine : int = ...

	CHANGE_NONE : int = ...

	CHANGE_X : int = ...

	CHANGE_Y : int = ...

	#: Set to true iff debug mode is used during compilation of the OGDF.
	debugMode : bool = ...

	firstAttribute : int = ...

	globalCounter : int = ...

	globalCounter : int = ...

	lpsolver_str : str = ...

	m_init : int = ...

	machineeps : float = ...

	mm_str : str = ...

	OGDF_GEOM_ET : EpsilonTest = ...

	rgbOfColor : int = ...

	s_ogdfInitializer : Initialization = ...

	s_random : std.mt19937 = ...

	s_randomMutex : std.mutex = ...

	strType : str = ...

	system_str : str = ...

	def addSegment(self, p : DPointHandle, q : DPointHandle, e : edge, vp : node, vq : node, xStructure : XSequence, original : Dict[DSegmentHandle,edge,DSegmentHash], internal : List[DSegmentHandle], segQueue : PrioritizedQueue[DSegmentHandle,DPointHandle], infinity : float) -> None:
		...

	def angleDistance(self, alpha : float, beta : float) -> float:
		...

	def angleNormalize(self, alpha : float) -> float:
		...

	def angleRangeAdapt(self, sectorStart : float, sectorEnd : float, start : float, length : float) -> None:
		...

	def angleSmaller(self, alpha : float, beta : float) -> bool:
		...

	def appendToList(self, adjList : SListPure[adjEntry], adj1 : adjEntry, BCtoG : AdjEntryArray[adjEntry], pos : AdjEntryArray[SListIterator[adjEntry] ]) -> None:
		...

	def areAdjacent(self, v : node, w : node) -> bool:
		...

	def atan2ex(self, y : float, x : float) -> float:
		...

	def bfs(self, v : node, newCluster : SList[node], visited : NodeArray[ bool ], C : ClusterGraph, rng : minstd_rand) -> None:
		...

	def bfs_SPAP(self, G : Graph, distance : NodeArray[NodeArray[ TCost ]], edgeCosts : TCost) -> None:
		"""Computes all-pairs shortest paths inGusing breadth-first serach (BFS)."""
		...

	def bfs_SPSS(self, s : node, G : Graph, distanceArray : NodeArray[ TCost ], edgeCosts : TCost) -> None:
		"""Computes single-source shortest paths fromsinGusing breadth-first search (BFS)."""
		...

	def bucketSort(self, a : Array[ E ], min : int, max : int, f : BucketFunc[ E ]) -> None:
		"""Bucket-sort arrayausing bucket assignmentf; the values offmust be in the interval [min,max]."""
		...

	def buffer_equal(self, buffer : str, str : str) -> bool:
		...

	def buildDfsTree(self, root : node, number : NodeArray[  int ], parent : NodeArray[node], childNr : NodeArray[  int ], revS : ArrayBuffer[node], directed : bool = False, firstNr : int = 1) -> int:
		"""Build up a dfs-tree starting from the node root by assigning each reachable node in the graph a discovery time (number) and a parent."""
		...

	def cconnect(self, CG : ClusterGraph, origCluster : NodeArray[cluster], oCcluster : ClusterArray[cluster], origNode : NodeArray[node], G : Graph, newEdges : List[NodePair]) -> None:
		...

	def cConnectTest(self, C : ClusterGraph, act : cluster, mark : NodeArray[ bool ], G : Graph) -> bool:
		...

	def chainsTwoEdgeConnected(self, graph : Graph, bridge : edge, dfsOrder : List[node], prev : NodeArray[edge], backEdges : NodeArray[ArrayBuffer[edge]]) -> bool:
		"""Helper function forogdf::isTwoEdgeConnected."""
		...

	def charCompareIgnoreCase(self, a : int, b : int) -> bool:
		...

	def checkSolution(self, matrixBegin : Array[  int ], matrixCount : Array[  int ], matrixIndex : Array[  int ], matrixValue : Array[ float ], rightHandSide : Array[ float ], equationSense : Array[  int ], lowerBound : Array[ float ], upperBound : Array[ float ], x : Array[ float ]) -> int:
		...

	@overload
	def chooseIteratorFrom(self, container : CONTAINER, includeElement : Callable = print, isFastTest : bool = True) -> CONTAINER.const_iterator:
		"""Returns an iterator to a random element in thecontainer."""
		...

	@overload
	def chooseIteratorFrom(self, container : CONTAINER, includeElement : Callable = print, isFastTest : bool = True) -> CONTAINER.iterator:
		"""Returns an iterator to a random element in thecontainer."""
		...

	def cMakeConnected(self, G : Graph, fullGraphCopy : Graph, fullGraphNode : NodeArray[node], badNode : NodeArray[ bool ], added : List[edge]) -> None:
		...

	def collapseCluster(self, CG : ClusterGraph, c : cluster, G : Graph) -> node:
		...

	def computeIntersection(self, xStructure : XSequence, yStructure : YSequence, sit0 : YSequence.iterator) -> None:
		...

	def computeSTNumbering(self, G : Graph, numbering : NodeArray[  int ], s : node = None, t : node = None, randomized : bool = False) -> int:
		"""Computes an st-Numbering ofG."""
		...

	def constructCConnectedCluster(self, v : node, C : ClusterGraph, rng : minstd_rand) -> None:
		...

	def constructCluster(self, v : node, C : ClusterGraph) -> None:
		...

	def copyPathsToSubdivision(self, paths : std.initializer_list[ TPath ], edges : TEdges) -> None:
		"""Copy paths to subdivision (auxiliary method)"""
		...

	def createClustersHelper(self, C : ClusterGraph, curr : node, pred : node, predC : cluster, internal : List[cluster], leaves : List[cluster]) -> None:
		...

	@overload
	def crossedEdge(self, adj : adjEntry) -> edge:
		...

	@overload
	def crossedEdge(self, adj : adjEntry) -> edge:
		...

	@overload
	def crossedEdge(self, adj : adjEntry) -> edge:
		...

	def defineGraphMLAttribute(self, xmlNode : pugi.xml_node, kind : str, name : str, type : str) -> None:
		...

	def defineGraphMLAttributes(self, xmlNode : pugi.xml_node, attributes : int) -> None:
		...

	def degreeDistribution(self, G : Graph, degdist : Array[  int ]) -> None:
		"""Fillsdegdistwith the degree distribution of graphG."""
		...

	def dfsGenTree(self, UG : UMLGraph, fakedGens : List[edge], fakeTree : bool) -> bool:
		...

	def dfsGenTreeRec(self, UG : UMLGraph, used : EdgeArray[ bool ], hierNumber : NodeArray[  int ], hierNum : int, v : node, fakedGens : List[edge], fakeTree : bool) -> bool:
		...

	def dfsMakeCConnected(self, v : node, source : node, visited : NodeArray[ bool ], badNode : NodeArray[ bool ], fullGraph : Graph, fullGraphCopy : NodeArray[node], keepsPlanarity : bool, vMinDeg : node) -> None:
		...

	def dfsTwoEdgeConnected(self, graph : Graph, dfsOrder : List[node], prev : NodeArray[edge], backEdges : NodeArray[ArrayBuffer[edge]]) -> bool:
		"""Helper function forogdf::isTwoEdgeConnectedFills up the output parametersdfsOrder,prevandbackEdges, by doing a dfs on thegraph."""
		...

	@overload
	def dijkstra_SPAP(self, G : Graph, shortestPathMatrix : NodeArray[NodeArray[ TCost ]], edgeCosts : EdgeArray[ TCost ]) -> None:
		"""Computes all-pairs shortest paths in graphGusing Dijkstra's algorithm."""
		...

	@overload
	def dijkstra_SPAP(self, GA : GraphAttributes, shortestPathMatrix : NodeArray[NodeArray[ TCost ]]) -> float:
		"""Computes all-pairs shortest paths inGAusing Dijkstra's algorithm."""
		...

	def dijkstra_SPSS(self, s : node, G : Graph, shortestPathMatrix : NodeArray[ TCost ], edgeCosts : EdgeArray[ TCost ]) -> None:
		"""Computes single-source shortest paths from nodesinGusing Disjkstra's algorithm."""
		...

	def doForEachCoordinate(self, PG : PlanRep, gl : GridLayout, func : Callable) -> None:
		...

	def dumpGraph(self, G : Graph) -> None:
		...

	def equalIgnoreCase(self, str1 : str, str2 : str) -> bool:
		"""Compares the two stringsstr1andstr2, ignoring the case of characters."""
		...

	def extractIdentifierLength(self, _from : str, start : str.size_type, line : int) -> str.size_type:
		...

	def fillPatternToString(self, fp : FillPattern) -> str:
		"""Converts fillpatternfpto string."""
		...

	def fillSignum(self, array : Array[  int ]) -> None:
		...

	def findCutVertices(self, number : NodeArray[  int ], parent : NodeArray[node], revS : ArrayBuffer[node], cutVertices : ArrayBuffer[node], addEdges : ArrayBuffer[Tuple2[node,node]], only_one : bool) -> bool:
		"""Find cut vertices and potential edges that could be added to turn the cut vertices into non-cut vertices."""
		...

	def findOpen(self, _from : str, line : int) -> str.size_type:
		...

	def findRoot(self, G : Graph) -> node:
		...

	def firstOutGen(self, UG : UMLGraph, v : node, _ : EdgeArray[ bool ]) -> edge:
		...

	def floydWarshall_SPAP(self, shortestPathMatrix : NodeArray[NodeArray[ TCost ]], G : Graph) -> None:
		"""Computes all-pairs shortest paths in graphGusing Floyd-Warshall's algorithm."""
		...

	def fromHex(self, c : int) -> int:
		...

	def fromString(self, key : str) -> ToClass:
		...

	def get_stacktrace(self, stream : std.ostream) -> None:
		...

	def getEdgeIndex(self, a : int, b : int, n : int, max : int) -> int:
		...

	def getMaxNumberEdges(self, n : int) -> int:
		...

	def getRepresentationNode(self, c : cluster) -> node:
		...

	def getRowIndex(self, j : int) -> int:
		"""Returns the base index of rowjfor an array containing a lower triangular matrix."""
		...

	def initFillPatternHashing(self) -> None:
		...

	def insertAfterList(self, adjList : SListPure[adjEntry], itBefore : SListIterator[adjEntry], adj1 : adjEntry, BCtoG : AdjEntryArray[adjEntry], pos : AdjEntryArray[SListIterator[adjEntry] ]) -> None:
		...

	def intToFillPattern(self, i : int) -> FillPattern:
		"""Converts integerito fill pattern."""
		...

	def intToStrokeType(self, i : int) -> StrokeType:
		"""Converts integerito stroke type."""
		...

	@overload
	def isBipartite(self, G : Graph) -> bool:
		"""Checks whether a graph is bipartite."""
		...

	@overload
	def isBipartite(self, G : Graph, color : NodeArray[ bool ]) -> bool:
		"""Checks whether a graph is bipartite."""
		...

	def isinf(self, value : T) -> bool:
		...

	def isIsolated(self, v : node) -> bool:
		"""Return true iff all incident edges of the given node v are self-loops."""
		...

	def isPlanar(self, G : Graph) -> bool:
		"""Returns true, if G is planar, false otherwise."""
		...

	@overload
	def isRegular(self, G : Graph) -> bool:
		"""Checks if a graph is regular."""
		...

	@overload
	def isRegular(self, G : Graph, d : int) -> bool:
		"""Checks if a graph is d-regular."""
		...

	def isSTNumbering(self, G : Graph, st_no : NodeArray[  int ], max : int) -> bool:
		"""Tests, whether a numbering of the nodes is an st-numbering."""
		...

	def isSTPlanar(self, graph : Graph, s : node, t : node) -> bool:
		"""Returns whether G is s-t-planar (i.e."""
		...

	def leftOfSegment(self, segment : DSegment, p : DPoint, newLen : float, left : bool = True) -> DPoint:
		...

	def loss(self, e : edge, tmpMark : NodeArray[ bool ]) -> int:
		...

	def maxAbs(self, a : float, b : float, c : float, d : float) -> float:
		...

	def newStartPos(self, _from : str, p : str.size_type, line : int) -> str.size_type:
		...

	def nodeDistribution(self, G : Graph, degdist : Array[  int ], func : Callable) -> None:
		"""Fillsdistwith the distribution given by a functionfuncin graphG."""
		...

	@overload
	def OGDF_DECLARE_COMPARER(self, _ : CmpHead, _ : bEdge, _ : int, head : WTF_TYPE["x-]"]) -> None:
		...

	@overload
	def OGDF_DECLARE_COMPARER(self, _ : CmpTail, _ : bEdge, _ : int, tail : WTF_TYPE["x-]"]) -> None:
		...

	@overload
	def OGDF_DECLARE_COMPARER(self, _ : cmpWithKey, _ : withKey, _ : int, key : WTF_TYPE["x."]) -> None:
		...

	@overload
	def OGDF_GEOM_ET(self, _6 : WTF_TYPE["1.0e-"]) -> EpsilonTest:
		...

	@overload
	def __ne__(self, t1 : Tuple2[ E1, E2 ], t2 : Tuple2[ E1, E2 ]) -> bool:
		"""Inequality operator for 2-tuples."""
		...

	@overload
	def __ne__(self, lhs : int, rhs : BoyerMyrvoldPlanar.EmbeddingGrade) -> bool:
		...

	@overload
	def __and__(self, lhs : edgeType, rhs : UMLEdgeTypeConstants) -> edgeType:
		...

	@overload
	def __and__(self, lhs : edgeType, rhs : UMLEdgeTypePatterns) -> edgeType:
		...

	@overload
	def __and__(self, i : int, b : TopologyModule.Options) -> int:
		...

	@overload
	def __and__(self, lhs : int, rhs : DynamicBacktrack.KuratowskiFlag) -> int:
		...

	@overload
	def __and__(self, lhs : int, rhs : UMLOpt) -> int:
		...

	@overload
	def __and__(self, lhs : int, rhs : WInfo.MinorType) -> int:
		...

	@overload
	def __and__(self, lhs : UMLEdgeTypePatterns, rhs : edgeType) -> edgeType:
		...

	def __iand__(self, lhs : int, rhs : DynamicBacktrack.KuratowskiFlag) -> int:
		...

	def __iadd__(self, lhs : int, rhs : UMLOpt) -> int:
		...

	@overload
	def __lshift__(self, lhs : edgeType, rhs : UMLEdgeTypeOffsets) -> edgeType:
		...

	@overload
	def __lshift__(self, lhs : edgeType, rhs : UMLEdgeTypePatterns) -> edgeType:
		...

	@overload
	def __lshift__(self, os : std.ostream, c : cluster) -> std.ostream:
		...

	@overload
	def __lshift__(self, os : std.ostream, lps : Configuration.LPSolver) -> std.ostream:
		"""Output operator forConfiguration::LPSolver(usesConfiguration::toString(Configuration::LPSolver))."""
		...

	@overload
	def __lshift__(self, os : std.ostream, mm : Configuration.MemoryManager) -> std.ostream:
		"""Output operator forConfiguration::MemoryManager(usesConfiguration::toString(Configuration::MemoryManager))."""
		...

	@overload
	def __lshift__(self, os : std.ostream, sys : Configuration.System) -> std.ostream:
		"""Output operator forConfiguration::System(usesConfiguration::toString(Configuration::System))."""
		...

	@overload
	def __lshift__(self, os : std.ostream, rs : BalloonLayout.RootSelection) -> std.ostream:
		...

	@overload
	def __lshift__(self, os : std.ostream, Q : BoundedQueue[ E,
	                        INDEX ]) -> std.ostream:
		"""PrintsBoundedQueueQto output streamos."""
		...

	@overload
	def __lshift__(self, os : std.ostream, dr : DIntersectableRect) -> std.ostream:
		...

	@overload
	def __lshift__(self, os : std.ostream, dop : DPolygon) -> std.ostream:
		"""Output operator for polygons."""
		...

	@overload
	def __lshift__(self, os : std.ostream, dr : DRect) -> std.ostream:
		...

	@overload
	def __lshift__(self, os : std.ostream, ea : EdgeArrow) -> std.ostream:
		"""Output operator."""
		...

	@overload
	def __lshift__(self, os : std.ostream, fp : FillPattern) -> std.ostream:
		"""Output operator."""
		...

	@overload
	def __lshift__(self, os : std.ostream, line : GenericLine[
	                        PointType ]) -> std.ostream:
		"""Output operator for lines."""
		...

	@overload
	def __lshift__(self, os : std.ostream, p : GenericPoint[ T
	                        ]) -> std.ostream:
		"""Output operator for generic points."""
		...

	@overload
	def __lshift__(self, os : std.ostream, dl : GenericSegment[
	                        PointType ]) -> std.ostream:
		"""Output operator for line segments."""
		...

	@overload
	def __lshift__(self, os : std.ostream, et : Graph.EdgeType) -> std.ostream:
		...

	@overload
	def __lshift__(self, os : std.ostream, i : GridPointInfo) -> std.ostream:
		...

	@overload
	def __lshift__(self, os : std.ostream, obj : KuratowskiWrapper.SubdivisionType) -> std.ostream:
		...

	@overload
	def __lshift__(self, os : std.ostream, n : LHTreeNode) -> std.ostream:
		...

	@overload
	def __lshift__(self, os : std.ostream, L : List[ E ]) -> std.ostream:
		"""Prints listLto output streamos."""
		...

	@overload
	def __lshift__(self, os : std.ostream, L : ListPure[ E ]) -> std.ostream:
		"""Prints listLto output streamos."""
		...

	@overload
	def __lshift__(self, os : std.ostream, r : Module.ReturnType) -> std.ostream:
		...

	@overload
	def __lshift__(self, os : std.ostream, np : NodePair) -> std.ostream:
		...

	@overload
	def __lshift__(self, os : std.ostream, a : ogdf.Array[ E, INDEX ]) -> std.ostream:
		"""Prints arrayato output streamos."""
		...

	@overload
	def __lshift__(self, os : std.ostream, a : ogdf.ArrayBuffer[
	                        E, INDEX ]) -> std.ostream:
		"""PrintsArrayBufferato output streamos."""
		...

	@overload
	def __lshift__(self, os : std.ostream, v : OptimalCrossingMinimizer.CrossingLocation) -> std.ostream:
		...

	@overload
	def __lshift__(self, os : std.ostream, v : OptimalCrossingMinimizer.CrossingVariable) -> std.ostream:
		...

	@overload
	def __lshift__(self, os : std.ostream, v : OrderedOptimalCrossingMinimizer.OrderedCrossingVariable) -> std.ostream:
		...

	@overload
	def __lshift__(self, os : std.ostream, v : OrderedOptimalCrossingMinimizer.SimpleCrossingVariable) -> std.ostream:
		...

	@overload
	def __lshift__(self, os : std.ostream, sc : PtrSuperCluster) -> std.ostream:
		...

	@overload
	def __lshift__(self, os : std.ostream, Q : Queue[ E ]) -> std.ostream:
		...

	@overload
	def __lshift__(self, os : std.ostream, Q : QueuePure[ E ]) -> std.ostream:
		...

	@overload
	def __lshift__(self, os : std.ostream, cr : RCCrossings) -> std.ostream:
		...

	@overload
	def __lshift__(self, os : std.ostream, L : SList[ E ]) -> std.ostream:
		"""Output operator."""
		...

	@overload
	def __lshift__(self, os : std.ostream, L : SListPure[ E ]) -> std.ostream:
		"""Output operator."""
		...

	@overload
	def __lshift__(self, os : std.ostream, stopwatch : Stopwatch) -> std.ostream:
		...

	@overload
	def __lshift__(self, os : std.ostream, st : StrokeType) -> std.ostream:
		"""Output operator."""
		...

	@overload
	def __lshift__(self, os : std.ostream, subset : SubsetEnumerator[
	                        T ]) -> std.ostream:
		...

	@overload
	def __lshift__(self, os : std.ostream, t2 : Tuple2[ E1, E2 ]) -> std.ostream:
		"""Output operator for 2-tuples."""
		...

	@overload
	def __lshift__(self, os : std.ostream, diagramGraph : UmlDiagramGraph) -> std.ostream:
		...

	@overload
	def __lshift__(self, os : std.ostream, modelGraph : UmlModelGraph) -> std.ostream:
		"""Output operator forUmlModelGraph."""
		...

	@overload
	def __lshift__(self, os : std.ostream, level : Logger.Level) -> std.ostream:
		...

	@overload
	def __lshift__(self, os : std.ostream, adj : ogdf.adjEntry) -> std.ostream:
		"""Output operator for adjacency entries; prints node and twin indices (or "nil")."""
		...

	@overload
	def __lshift__(self, os : std.ostream, e : ogdf.edge) -> std.ostream:
		"""Output operator for edges; prints source and target indices (or "nil")."""
		...

	@overload
	def __lshift__(self, os : std.ostream, e : ogdf.hyperedge) -> std.ostream:
		...

	@overload
	def __lshift__(self, os : std.ostream, H : ogdf.Hypergraph) -> std.ostream:
		...

	@overload
	def __lshift__(self, os : std.ostream, v : ogdf.hypernode) -> std.ostream:
		...

	@overload
	def __lshift__(self, os : std.ostream, v : ogdf.node) -> std.ostream:
		"""Output operator for nodes; prints node index (or "nil")."""
		...

	@overload
	def __lshift__(self, os : std.ostream, k : OptimalCrossingMinimizer.KuratowskiConstraint) -> std.ostream:
		...

	@overload
	def __lshift__(self, os : std.ostream, k : OptimalCrossingMinimizer.SimplicityConstraint) -> std.ostream:
		...

	@overload
	def __lshift__(self, os : std.ostream, k : OrderedOptimalCrossingMinimizer.BasicKuratowskiConstraint) -> std.ostream:
		...

	@overload
	def __lshift__(self, lhs : UMLEdgeTypeConstants, rhs : UMLEdgeTypeOffsets) -> edgeType:
		...

	@overload
	def __lshift__(self, lhs : UMLNodeTypeConstants, rhs : UMLNodeTypeOffsets) -> int:
		...

	def __le__(self, lhs : int, rhs : BoyerMyrvoldPlanar.EmbeddingGrade) -> bool:
		...

	@overload
	def __eq__(self, t1 : Tuple2[ E1, E2 ], t2 : Tuple2[ E1, E2 ]) -> bool:
		"""Equality operator for 2-tuples."""
		...

	@overload
	def __eq__(self, lhs : edgeType, rhs : UMLEdgeTypeConstants) -> bool:
		...

	@overload
	def __eq__(self, lhs : int, rhs : BoyerMyrvoldPlanar.EmbeddingGrade) -> bool:
		...

	def __gt__(self, lhs : int, rhs : BoyerMyrvoldPlanar.EmbeddingGrade) -> bool:
		...

	@overload
	def __rshift__(self, lhs : edgeType, rhs : UMLEdgeTypeOffsets) -> edgeType:
		...

	@overload
	def __rshift__(self, _is : std.istream, H : ogdf.Hypergraph) -> std.istream:
		...

	@overload
	def __rshift__(self, _is : std.istream, token : TokenIgnorer) -> std.istream:
		...

	@overload
	def __or__(self, i : int, b : TopologyModule.Options) -> int:
		...

	@overload
	def __or__(self, lhs : int, rhs : UMLOpt) -> int:
		...

	@overload
	def __or__(self, a : TopologyModule.Options, b : TopologyModule.Options) -> int:
		...

	@overload
	def __ior__(self, lhs : int, rhs : DynamicBacktrack.KuratowskiFlag) -> int:
		...

	@overload
	def __ior__(self, lhs : int, rhs : WInfo.MinorType) -> int:
		...

	@overload
	def __ior__(self, i : int, fm : CPUFeatureMask) -> int:
		...

	@overload
	def __invert__(self, rhs : DynamicBacktrack.KuratowskiFlag) -> int:
		...

	@overload
	def __invert__(self, rhs : UMLOpt) -> int:
		...

	@overload
	def orientation(self, p : DPoint, q : DPoint, r : DPoint) -> int:
		...

	@overload
	def orientation(self, p : DPointHandle, q : DPointHandle, r : DPointHandle) -> int:
		...

	@overload
	def orientation(self, s : DSegment, p : DPoint) -> int:
		...

	@overload
	def orientation(self, seg : DSegmentHandle, p : DPointHandle) -> int:
		...

	def outputPG(self, PG : PlanRepExpansion, i : int) -> None:
		...

	def outputRegions(self, regions : List[SCRegion]) -> None:
		...

	def planarEmbed(self, G : Graph) -> bool:
		"""Returns true, if G is planar, false otherwise. If true is returned, G will be planarly embedded."""
		...

	def planarEmbedPlanarGraph(self, G : Graph) -> bool:
		"""Constructs a planar embedding of G. It assumes thatGis planar!"""
		...

	def planarSTEmbed(self, graph : Graph, s : node, t : node) -> bool:
		"""s-t-planarly embeds a graph."""
		...

	def prefixIgnoreCase(self, prefix : str, str : str) -> bool:
		"""Tests ifprefixis a prefix ofstr, ignoring the case of characters."""
		...

	def preprocessStep(self, C : ClusterGraph, G : Graph) -> bool:
		...

	@overload
	def print(self, os : std.ostream, a : Array[ E, INDEX ], delim : int = ' ') -> None:
		"""Prints arrayato output streamosusing delimiterdelim."""
		...

	@overload
	def print(self, os : std.ostream, a : ArrayBuffer[ E,
	                        INDEX ], delim : int = ' ') -> None:
		"""PrintsArrayBufferato output streamosusing delimiterdelim."""
		...

	@overload
	def print(self, os : std.ostream, L : List[ E ], delim : int = ' ') -> None:
		"""Prints listLto output streamosusing delimiterdelim."""
		...

	@overload
	def print(self, os : std.ostream, L : ListPure[ E ], delim : int = ' ') -> None:
		"""Prints listLto output streamosusing delimiterdelim."""
		...

	@overload
	def print(self, os : std.ostream, Q : Queue[ E ], delim : int = ' ') -> None:
		...

	@overload
	def print(self, os : std.ostream, Q : QueuePure[ E ], delim : int = ' ') -> None:
		...

	@overload
	def print(self, os : std.ostream, L : SList[ E ], delim : int = ' ') -> None:
		"""Prints listLto output streamosusing delimiterdelim."""
		...

	@overload
	def print(self, os : std.ostream, L : SListPure[ E ], delim : int = ' ') -> None:
		"""Prints listLto output streamosusing delimiterdelim."""
		...

	@overload
	def printCCGx(self, filename : str, D : CompactionConstraintGraph[  int ], drawing : GridLayoutMapped) -> None:
		...

	@overload
	def printCCGx(self, filename : str, D : GridCompactionConstraintGraph[  int ], drawing : GridLayout) -> None:
		...

	@overload
	def printCCGy(self, filename : str, D : CompactionConstraintGraph[  int ], drawing : GridLayoutMapped) -> None:
		...

	@overload
	def printCCGy(self, filename : str, D : GridCompactionConstraintGraph[  int ], drawing : GridLayout) -> None:
		...

	@overload
	def quicksortTemplate(self, L : LIST) -> None:
		...

	@overload
	def quicksortTemplate(self, L : LIST, comp : COMPARER) -> None:
		...

	def randomDouble(self, low : float, high : float) -> float:
		"""Returns a random double value from the interval [low,high)."""
		...

	def randomDoubleNormal(self, m : float, sd : float) -> float:
		"""Returns a random double value from the normal distribution with mean m and standard deviation sd."""
		...

	def randomNumber(self, low : int, high : int) -> int:
		"""Returns random integer between low and high (including)."""
		...

	def randomSeed(self) -> int:
		"""Returns a random value suitable as initial seed for a random number engine."""
		...

	def randomSimpleGraphByMask(self, G : Graph, n : int, m : int, preEdges : Array[ bool ], preAdded : int = 0) -> bool:
		"""Auxiliary function forogdf::randomSimpleGraphandogdf::randomSimpleConnectedGraph."""
		...

	def randomSimpleGraphBySet(self, G : Graph, n : int, m : int, preEdges : List[ std.pair[  int,  int ]]) -> bool:
		"""Auxiliary function forogdf::randomSimpleGraphandogdf::randomSimpleConnectedGraph."""
		...

	def read_next_line(self, _is : std.istream, buffer : str) -> bool:
		...

	def readDigraph6WithForcedHeader(self, G : Graph, _is : std.istream) -> bool:
		...

	def readDigraph6WithoutForcedHeader(self, G : Graph, _is : std.istream) -> bool:
		...

	def readEdgeListRow(self, _is : std.istringstream, G : Graph, GA : GraphAttributes, v : node, u : node) -> bool:
		...

	def readGraph6WithForcedHeader(self, G : Graph, _is : std.istream) -> bool:
		...

	def readGraph6WithoutForcedHeader(self, G : Graph, _is : std.istream) -> bool:
		...

	def readMatrixRow(self, _is : std.istream, G : Graph, GA : GraphAttributes, v : node) -> bool:
		...

	def readSparse6WithForcedHeader(self, G : Graph, _is : std.istream) -> bool:
		...

	def readSparse6WithoutForcedHeader(self, G : Graph, _is : std.istream) -> bool:
		...

	def recursiveCConnect(self, CG : ClusterGraph, act : cluster, origCluster : NodeArray[cluster], oCcluster : ClusterArray[cluster], origNode : NodeArray[node], G : Graph, fullCopy : Graph, copyNode : NodeArray[node], badNode : NodeArray[ bool ], newEdges : List[NodePair]) -> None:
		...

	def recursiveConnect(self, CG : ClusterGraph, act : cluster, origCluster : NodeArray[cluster], oCcluster : ClusterArray[cluster], origNode : NodeArray[node], G : Graph, newEdges : List[NodePair]) -> None:
		...

	@overload
	def removeTrailingWhitespace(self, str : str) -> None:
		...

	@overload
	def removeTrailingWhitespace(self, str : str) -> None:
		"""Removes trailing space, horizontal and vertical tab, feed, newline, and carriage return fromstr."""
		...

	def reverse(self, container : T) -> Reverse[ T ]:
		"""Provides iterators forcontainerto make it easily iterable in reverse."""
		...

	def safeForEach(self, container : CONTAINER, func : Callable) -> None:
		"""Calls (possibly destructive)funcfor each element ofcontainer."""
		...

	def safeTestForEach(self, container : CONTAINER, func : Callable) -> bool:
		"""Likeogdf::safeForEach()but aborts iffuncreturnsfalse."""
		...

	def searchPos(self, C : CONTAINER, x : T) -> int:
		"""Searches for the position ofxin containerC; returns -1 if not found."""
		...

	def segment(self, bends : DPolyline, fraction : float) -> DSegment:
		...

	def setSeed(self, val : int) -> None:
		"""Sets the seed for functions likerandomSeed(),randomNumber(),randomDouble()."""
		...

	def shapeToString(self, s : Shape) -> str:
		"""Converts shapesto string."""
		...

	def stPath(self, path : ArrayBuffer[node], v : node, adj : adjEntry, markedNode : NodeArray[ bool ], markedEdge : EdgeArray[ bool ], dfn : NodeArray[  int ], dfsInEdge : NodeArray[edge], followLowPath : NodeArray[edge]) -> bool:
		...

	def stringToFillPattern(self, s : str) -> FillPattern:
		"""Converts stringsto fill pattern."""
		...

	def stringToShape(self, s : str) -> Shape:
		"""Converts stringsto shape."""
		...

	def stringToStrokeType(self, s : str) -> StrokeType:
		"""Converts stringsto stroke type."""
		...

	def strokeTypeToString(self, st : StrokeType) -> str:
		"""Converts stringsto stroke type."""
		...

	def stSearch(self, G : Graph, v : node, count : int, low : NodeArray[  int ], dfn : NodeArray[  int ], dfsInEdge : NodeArray[edge], followLowPath : NodeArray[edge]) -> None:
		...

	def toEnum(self, str : str, toString : str, first : E, last : E, _def : E) -> E:
		...

	def tohex(self, value : int) -> int:
		...

	def toString(self, key : FromClass) -> str:
		...

	def usedTime(self, T : float) -> float:
		"""Returns used CPU time from T to current time and assigns current time to T."""
		...

	@overload
	def write_gml_cluster(self, c : cluster, d : int, os : std.ostream, index : NodeArray[  int ], nextClusterIndex : int) -> None:
		...

	@overload
	def write_gml_cluster(self, CA : ClusterGraphAttributes, c : cluster, d : int, os : std.ostream, index : NodeArray[  int ], nextClusterIndex : int) -> None:
		...

	def write_gml_footer(self, os : std.ostream) -> None:
		...

	@overload
	def write_gml_graph(self, G : Graph, os : std.ostream, index : NodeArray[  int ]) -> None:
		...

	@overload
	def write_gml_graph(self, A : GraphAttributes, os : std.ostream, index : NodeArray[  int ]) -> None:
		...

	def write_gml_header(self, os : std.ostream, directed : bool) -> None:
		...

	@overload
	def writeCcgGML(self, D : CompactionConstraintGraph[  int ], AG : GraphAttributes, filename : str) -> None:
		...

	@overload
	def writeCcgGML(self, D : GridCompactionConstraintGraph[  int ], AG : GraphAttributes, filename : str) -> None:
		...

	def writeEdges(self, os : std.ostream, G : Graph, GA : GraphAttributes, index : NodeArray[  int ]) -> None:
		...

	def writeGraph(self, os : std.ostream, G : Graph, GA : GraphAttributes) -> bool:
		...

	def writeGraphMLAttribute(self, xmlNode : pugi.xml_node, name : str, value : T) -> None:
		...

	@overload
	def writeGraphMLCluster(self, xmlNode : pugi.xml_node, C : ClusterGraph, c : cluster) -> None:
		...

	@overload
	def writeGraphMLCluster(self, xmlNode : pugi.xml_node, CA : ClusterGraphAttributes, c : cluster) -> None:
		...

	@overload
	def writeGraphMLEdge(self, xmlNode : pugi.xml_node, e : edge) -> pugi.xml_node:
		...

	@overload
	def writeGraphMLEdge(self, xmlNode : pugi.xml_node, GA : GraphAttributes, e : edge) -> None:
		...

	def writeGraphMLHeader(self, doc : pugi.xml_document) -> pugi.xml_node:
		...

	@overload
	def writeGraphMLNode(self, xmlNode : pugi.xml_node, GA : GraphAttributes, v : node) -> None:
		...

	@overload
	def writeGraphMLNode(self, xmlNode : pugi.xml_node, v : node) -> None:
		...

	def writeGraphTag(self, xmlNode : pugi.xml_node, edgeDefault : str) -> pugi.xml_node:
		...

	@overload
	def writeGridDrawing(self, name : str, PG : PlanRep, drawing : GridLayout) -> None:
		...

	@overload
	def writeGridDrawing(self, name : str, PG : PlanRep, drawing : GridLayoutMapped) -> None:
		...

	def writeLongString(self, os : std.ostream, str : str) -> None:
		...

	def writeMatrix(self, os : std.ostream, G : Graph, GA : GraphAttributes, index : NodeArray[  int ]) -> None:
		...
