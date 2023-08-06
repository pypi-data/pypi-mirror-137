# file stubs/ogdf/MinSteinerTreeModule.py generated from classogdf_1_1_min_steiner_tree_module
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
T = TypeVar('T')

class MinSteinerTreeModule(Generic[T]):

	"""Serves as an interface for various methods to compute or approximate minimum Steiner trees on undirected graphs with edge costs."""

	# Auxiliary post-processing functions

	def pruneAllDanglingSteinerPaths(self, steinerTree : EdgeWeightedGraphCopy[ T ], isTerminal : NodeArray[ bool ]) -> T:
		"""Prunes nonterminal leaves and their paths to terminal or branching nodes."""
		...

	def pruneDanglingSteinerPathFrom(self, steinerTree : EdgeWeightedGraphCopy[ T ], isTerminal : NodeArray[ bool ], start : node) -> T:
		"""Prunes the dangling Steiner path beginning at a given nonterminal leaf only."""
		...

	def pruneDanglingSteinerPathsFrom(self, steinerTree : EdgeWeightedGraphCopy[ T ], isTerminal : NodeArray[ bool ], start : List[node]) -> T:
		"""Prunes dangling Steiner paths beginning at given nonterminal leaves only."""
		...

	def removeCyclesFrom(self, steinerTree : EdgeWeightedGraphCopy[ T ], isTerminal : NodeArray[ bool ]) -> T:
		"""Remove remaining cycles from a Steiner "almost" tree."""
		...

	# Special SSSP and APSP algorithms used in component-based approximation algorithms

	def singleSourceShortestPathsPreferringTerminals(self, G : EdgeWeightedGraph[ T ], source : node, isTerminal : NodeArray[ bool ], distance : NodeArray[ T ], pred : NodeArray[edge]) -> None:
		"""Modified single-source-shortest-paths (Dijkstra) with heuristic to prefer paths over terminals."""
		...

	def singleSourceShortestPathsStandard(self, G : EdgeWeightedGraph[ T ], source : node, _ : NodeArray[ bool ], distance : NodeArray[ T ], pred : NodeArray[edge]) -> None:
		"""Standard single-source-shortest-paths algoritm (Dijkstra)"""
		...

	def singleSourceShortestPaths(self, G : EdgeWeightedGraph[ T ], source : node, isTerminal : NodeArray[ bool ], distance : NodeArray[ T ], pred : NodeArray[edge]) -> None:
		"""The default single-source-shortest-paths algorithm."""
		...

	def allTerminalShortestPathsStandard(self, G : EdgeWeightedGraph[ T ], terminals : List[node], isTerminal : NodeArray[ bool ], distance : NodeArray[NodeArray[ T ]], pred : NodeArray[NodeArray[edge]]) -> None:
		"""RunssingleSourceShortestPathsStandardfrom all terminals."""
		...

	def allTerminalShortestPathsPreferringTerminals(self, G : EdgeWeightedGraph[ T ], terminals : List[node], isTerminal : NodeArray[ bool ], distance : NodeArray[NodeArray[ T ]], pred : NodeArray[NodeArray[edge]]) -> None:
		"""RunssingleSourceShortestPathsPreferringTerminalsfrom all terminals."""
		...

	def allTerminalShortestPaths(self, G : EdgeWeightedGraph[ T ], terminals : List[node], isTerminal : NodeArray[ bool ], distance : NodeArray[NodeArray[ T ]], pred : NodeArray[NodeArray[edge]], ssspFunc : Callable = print) -> None:
		"""Runs a given (or the default) single-source-shortest-paths function from all terminals."""
		...

	def allNodeShortestPathsStandard(self, G : EdgeWeightedGraph[ T ], terminals : List[node], isTerminal : NodeArray[ bool ], distance : NodeArray[NodeArray[ T ]], pred : NodeArray[NodeArray[edge]]) -> None:
		"""RunssingleSourceShortestPathsStandardfrom all nodes."""
		...

	def allNodeShortestPathsPreferringTerminals(self, G : EdgeWeightedGraph[ T ], terminals : List[node], isTerminal : NodeArray[ bool ], distance : NodeArray[NodeArray[ T ]], pred : NodeArray[NodeArray[edge]]) -> None:
		"""RunssingleSourceShortestPathsPreferringTerminalsfrom all nodes."""
		...

	def allNodeShortestPaths(self, G : EdgeWeightedGraph[ T ], terminals : List[node], isTerminal : NodeArray[ bool ], distance : NodeArray[NodeArray[ T ]], pred : NodeArray[NodeArray[edge]], ssspFunc : Callable = print) -> None:
		"""Runs a given (or the default) single-source-shortest-paths function from all nodes."""
		...

	def allPairShortestPathsPreferringTerminals(self, G : EdgeWeightedGraph[ T ], isTerminal : NodeArray[ bool ], distance : NodeArray[NodeArray[ T ]], pred : NodeArray[NodeArray[edge]]) -> None:
		"""Modified all-pair-shortest-paths algorithm (Floyd-Warshall) with heuristic to prefer paths over terminals."""
		...

	def allPairShortestPathsStandard(self, G : EdgeWeightedGraph[ T ], _ : NodeArray[ bool ], distance : NodeArray[NodeArray[ T ]], pred : NodeArray[NodeArray[edge]]) -> None:
		"""Standard all-pair-shortest-paths algorithm (Floyd-Warshall)"""
		...

	def allPairShortestPaths(self, G : EdgeWeightedGraph[ T ], isTerminal : NodeArray[ bool ], distance : NodeArray[NodeArray[ T ]], pred : NodeArray[NodeArray[edge]]) -> None:
		"""The default all-pair-shortest-paths algorithm."""
		...

	# Drawings for debugging

	@overload
	def drawSVG(self, G : EdgeWeightedGraph[ T ], isTerminal : NodeArray[ bool ], steinerTree : EdgeWeightedGraphCopy[ T ], filename : str) -> None:
		"""Writes an SVG file of a minimum Steiner tree in the original graph."""
		...

	@overload
	def drawSVG(self, G : EdgeWeightedGraph[ T ], isTerminal : NodeArray[ bool ], filename : str) -> None:
		"""Writes an SVG file of the instance graph."""
		...

	def drawSteinerTreeSVG(self, steinerTree : EdgeWeightedGraphCopy[ T ], isTerminal : NodeArray[ bool ], filename : str) -> None:
		"""Writes a SVG that shows only the given Steiner tree."""
		...

	def __destruct__(self) -> None:
		"""Do nothing on destruction."""
		...

	def call(self, G : EdgeWeightedGraph[ T ], terminals : List[node], isTerminal : NodeArray[ bool ], finalSteinerTree : EdgeWeightedGraphCopy[ T ]) -> T:
		"""Calls the Steiner tree algorithm for nontrivial cases but handles trivial cases directly."""
		...

	def getNonterminals(self, nonterminals : ArrayBuffer[node], G : EdgeWeightedGraph[ T ], isTerminal : NodeArray[ bool ]) -> None:
		"""Generates a list (as ArrayBuffer<node>) of all nonterminals."""
		...

	def getTerminals(self, terminals : List[node], G : EdgeWeightedGraph[ T ], isTerminal : NodeArray[ bool ]) -> None:
		"""Generates a list (asList<node>) of all terminals."""
		...

	def isQuasiBipartite(self, G : EdgeWeightedGraph[ T ], isTerminal : NodeArray[ bool ]) -> bool:
		"""Checks in O(n + m) time if a given Steiner tree problem instance is quasi-bipartite."""
		...

	def isSteinerTree(self, G : EdgeWeightedGraph[ T ], terminals : List[node], isTerminal : NodeArray[ bool ], steinerTree : EdgeWeightedGraphCopy[ T ]) -> bool:
		"""Checks in O(n) time if a given tree is acually a Steiner Tree."""
		...

	def sortTerminals(self, terminals : List[node]) -> None:
		"""Sort terminals by index."""
		...

	def computeSteinerTree(self, G : EdgeWeightedGraph[ T ], terminals : List[node], isTerminal : NodeArray[ bool ], finalSteinerTree : EdgeWeightedGraphCopy[ T ]) -> T:
		"""Computes the actual Steiner tree."""
		...
