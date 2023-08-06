# file stubs/ogdf/SteinerTreePreprocessing.py generated from classogdf_1_1_steiner_tree_preprocessing
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
LAMBDA = TypeVar('LAMBDA')

TWhat = TypeVar('TWhat')

T = TypeVar('T')

TWhatArray = TypeVar('TWhatArray')

class SteinerTreePreprocessing(Generic[T]):

	"""This class implements preprocessing strategies for the Steiner tree problem."""

	# Methods on Steiner tree instances

	def getReducedGraph(self) -> EdgeWeightedGraph[ T ]:
		"""Returns the reduced form of the graph."""
		...

	def getReducedTerminals(self) -> List[node]:
		"""Returns the list of the terminals corresponding to the reduced graph."""
		...

	def shuffleReducedTerminals(self) -> None:
		"""Shuffles the list of reduced terminals. This can have an effect on some tests."""
		...

	def getReducedIsTerminal(self) -> NodeArray[ bool ]:
		"""Returns theNodeArray<bool>isTerminal corresponding to the reduced graph."""
		...

	# Methods for Steiner tree solutions

	def costEdgesAlreadyInserted(self) -> T:
		"""Returns the cost of the edges already inserted in solution during the reductions."""
		...

	def computeOriginalSolution(self, reducedGraphSolution : EdgeWeightedGraphCopy[ T ], correspondingOriginalSolution : EdgeWeightedGraphCopy[ T ]) -> None:
		"""Computes the solution for the original graph, given a solution on the reduction."""
		...

	# Combined reduction sets

	def reduceTrivial(self) -> bool:
		"""Apply trivial (hence amazingly fast) reductions iteratively, that isdegree2Test(),makeSimple(),deleteLeaves()."""
		...

	def reduceFast(self) -> bool:
		"""Apply fast reductions iteratively (includes trivial reductions)."""
		...

	def reduceFastAndDualAscent(self) -> bool:
		"""Apply fast reductions and the dual-ascent-based tests iteratively."""
		...

	# Single reductions

	def deleteLeaves(self) -> bool:
		"""Deletes the leaves of the graph."""
		...

	def makeSimple(self) -> bool:
		"""Deletes parallel edges keeping only the minimum cost one, and deletes self-loops."""
		...

	def deleteComponentsWithoutTerminals(self) -> bool:
		"""Deletes connected components with no terminals."""
		...

	def leastCostTest(self) -> bool:
		"""Performs a least cost test [DV89] computing the whole shortest path matrix."""
		...

	def degree2Test(self) -> bool:
		"""deletes degree-2 nodes and replaces them with one edge with the adjacent edges' sum"""
		...

	def PTmTest(self, k : int = 3) -> bool:
		""""Paths with many terminals" test, efficient on paths with many terminals."""
		...

	def terminalDistanceTest(self) -> bool:
		"""Simple terminal distance test [PV01]."""
		...

	def longEdgesTest(self) -> bool:
		"""Long-Edges test from [DV89]."""
		...

	def NTDkTest(self, maxTestedDegree : int = 5, k : int = 3) -> bool:
		"""Non-terminals of degree k test [DV89, PV01]."""
		...

	def nearestVertexTest(self) -> bool:
		"""Nearest vertex test usingVoronoiregions [DV89, PV01]."""
		...

	def shortLinksTest(self) -> bool:
		"""Short links test usingVoronoiregions [PV01]."""
		...

	@overload
	def lowerBoundBasedTest(self, upperBound : T) -> bool:
		"""Computes for each non-terminal a lower bound of the cost of the minimum Steiner tree containing it."""
		...

	@overload
	def lowerBoundBasedTest(self) -> bool:
		"""LikelowerBoundBasedTest(T upperBound)but the upper bound is computed bycomputeMinSteinerTreeUpperBound."""
		...

	@overload
	def dualAscentBasedTest(self, repetitions : int, upperBound : T) -> bool:
		"""LikelowerBoundBasedTest(T upperBound)but usesogdf::SteinerTreeLowerBoundDualAscentto compute lower bounds."""
		...

	@overload
	def dualAscentBasedTest(self, repetitions : int = 1) -> bool:
		"""LikedualAscentBasedTest(int repetitions, T upperBound)but the upper bound is computed bycomputeMinSteinerTreeUpperBound."""
		...

	def reachabilityTest(self, maxDegreeTest : int = 0, k : int = 3) -> bool:
		"""Performs a reachability test [DV89]."""
		...

	def cutReachabilityTest(self) -> bool:
		"""Performs a cut reachability test [DV89]."""
		...

	# Miscellaneous methods

	def setCostUpperBoundAlgorithm(self, pMinSteinerTreeModule : MinSteinerTreeModule[ T ]) -> None:
		"""Set the module option for the algorithm used for computing the MinSteinerTree cost upper bound."""
		...

	def repeat(self, f : Callable) -> bool:
		"""Auxiliary function: Repeats a function until it returns false (used for iteratively applying reductions)"""
		...

	def addNew(self, x : TWhat, replacedNodes : List[node], replacedEdges : List[edge], deleteReplacedElements : bool, whatSonsListIndex : TWhatArray) -> None:
		"""Update internal data structures to let a (new) node or edge represent replaced nodes and/or edges."""
		...

	def addNewNode(self, v : node, replacedNodes : List[node], replacedEdges : List[edge], deleteReplacedElements : bool) -> None:
		"""CallsaddNew()for a node."""
		...

	def addNewEdge(self, e : edge, replacedNodes : List[node], replacedEdges : List[edge], deleteReplacedElements : bool) -> None:
		"""The function is called after a new edge is added to the copy graph during the reductions."""
		...

	def addEdgesToSolution(self, edgesToBeAddedInSolution : List[edge]) -> bool:
		"""The function adds a set of edges in the solution."""
		...

	def recomputeTerminalsList(self) -> None:
		"""Used by reductions to recompute the m_copyTerminals list, according to m_copyIsTerminal; useful when "online" updates to m_copyTerminals are inefficient."""
		...

	def computeShortestPathMatrix(self, shortestPath : NodeArray[NodeArray[ T ]]) -> None:
		"""Computes the shortest path matrix corresponding to the m_copyGraph."""
		...

	def floydWarshall(self, shortestPath : NodeArray[NodeArray[ T ]]) -> None:
		"""Applies the Floyd-Warshall algorithm on the m_copyGraph. The shortestPath matrix has to be already initialized."""
		...

	@overload
	def computeMinSteinerTreeUpperBound(self, finalSteinerTree : EdgeWeightedGraphCopy[ T ]) -> T:
		...

	@overload
	def computeMinSteinerTreeUpperBound(self) -> T:
		...

	def addToSolution(self, listIndex : int, isInSolution : Array[ bool,  int ]) -> None:
		"""Helper method for computeOriginalSolution."""
		...

	def deleteNodesAboveUpperBound(self, lowerBoundWithNode : NodeArray[ T ], upperBound : T) -> bool:
		"""Deletes the nodes whose lowerBoundWithNode exceeds upperBound."""
		...

	def deleteEdgesAboveUpperBound(self, lowerBoundWithEdge : EdgeArray[ T ], upperBound : T) -> bool:
		"""Deletes the edges whose lowerBoundWithEdge exceeds upperBound."""
		...

	def deleteSteinerDegreeTwoNode(self, v : node, tprime : EdgeWeightedGraphCopy[ T ], tprimeHPD : steiner_tree.HeavyPathDecomposition[ T ], closestTerminals : NodeArray[List[ std.pair[node, T ]]]) -> None:
		"""Deletes a node that is known to have degree 2 in at least one minimum Steiner tree."""
		...

	def findClosestNonTerminals(self, source : node, reachedNodes : List[node], distance : NodeArray[ T ], maxDistance : T, expandedEdges : int) -> None:
		"""Heuristic approach to computing the closest non-terminals for one node, such that there is no terminal on the path from it to a "close non-terminal" and a maximum constant number of expandedEdges are expanded during the computation."""
		...

	def computeBottleneckDistance(self, x : node, y : node, tprime : EdgeWeightedGraphCopy[ T ], tprimeHPD : steiner_tree.HeavyPathDecomposition[ T ], closestTerminals : NodeArray[List[ std.pair[node, T ]]]) -> T:
		"""Heuristic computation [PV01] of the bottleneck Steiner distance between two nodes in a graph."""
		...

	def computeClosestKTerminals(self, k : int, closestTerminals : NodeArray[List[ std.pair[node, T ]]]) -> None:
		"""Computes for every non-terminal the closest k terminals such that there is no other terminal on the path."""
		...

	def computeRadiusOfTerminals(self, terminalRadius : NodeArray[ T ]) -> None:
		"""Compute radius of terminals."""
		...

	def computeRadiusSum(self) -> T:
		"""Compute the sum of all radii except the two largest."""
		...

	def computeOptimalTerminals(self, v : node, dist : LAMBDA, optimalTerminal1 : node, optimalTerminal2 : node, distance : NodeArray[ T ]) -> None:
		"""Compute first and second best terminals according to functiondist."""
		...

	def markSuccessors(self, currentNode : node, voronoiRegions : Voronoi[ T ], isSuccessorOfMinCostEdge : NodeArray[ bool ]) -> None:
		"""Mark successors ofcurrentNodein its shortest-path tree invoronoiRegions."""
		...

	def findTwoMinimumCostEdges(self, v : node, first : edge, second : edge) -> None:
		"""Finds thefirstandsecondsmallest edges incident tov."""
		...

	#: Copy of the original graph; this copy will actually be reduced.
	m_copyGraph : EdgeWeightedGraph[ T ] = ...

	#: The reduced form of isTerminal.
	m_copyIsTerminal : NodeArray[ bool ] = ...

	#: The reduced form of terminals.
	m_copyTerminals : List[node] = ...

	#: The cost of the already inserted in solution edges.
	m_costAlreadyInserted : T = ...

	#: Algorithm used for computing the upper bound for the cost of a minimum Steiner tree.
	m_costUpperBoundAlgorithm : std.unique_ptr[MinSteinerTreeModule[ T ] ] = ...

	#: See m_nodeSonsListIndex but for edges.
	m_edgeSonsListIndex : EdgeArray[  int ] = ...

	m_eps : EpsilonTest = ...

	#: It contains for each node an index i.
	m_nodeSonsListIndex : NodeArray[  int ] = ...

	#: Const reference to the original graph.
	m_origGraph : EdgeWeightedGraph[ T ] = ...

	#: Const reference to the original isTerminal.
	m_origIsTerminal : NodeArray[ bool ] = ...

	#: Const reference to the original list of terminals.
	m_origTerminals : List[node] = ...

	#: Listwith lists (corresponding to nodes and containing the indexes of their sons)
	m_sonsList : List[ List[  int ] ] = ...

	def __init__(self, wg : EdgeWeightedGraph[ T ], terminals : List[node], isTerminal : NodeArray[ bool ]) -> None:
		...

	def solve(self, mst : MinSteinerTreeModule[ T ], finalSteinerTree : EdgeWeightedGraphCopy[ T ]) -> T:
		"""A shortcut to get the solution of a reduced instance."""
		...
