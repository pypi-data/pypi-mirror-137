# file stubs/ogdf/MinSteinerTreeZelikovsky.py generated from classogdf_1_1_min_steiner_tree_zelikovsky
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
T = TypeVar('T')

TYPE = TypeVar('TYPE')

class MinSteinerTreeZelikovsky(ogdf.MinSteinerTreeModule[ T ], Generic[T]):

	"""This class implements the 11/6-approximation algorithm by Zelikovsky for the minimum Steiner tree problem along with variants and practical improvements."""

	class Pass(enum.Enum):

		"""Enables a heuristic version (for TG exhaustive and voronoi only)"""

		#: heuristic: evaluate all triples, sort them descending by gain, traverse sorted triples once, contract when possible
		one = enum.auto()

		#: normal, greedy version
		multi = enum.auto()

	Save : Type = steiner_tree.Save[ TYPE ]

	class SaveCalculation(enum.Enum):

		"""Different methods for obtaining save edges."""

		#: Stores explicitly the save edge for every pair of terminals. Needs O(n^2) space but has fast query times.
		staticEnum = enum.auto()

		#: Builds a "weight tree" (save edges are inner nodes, terminals are leaves and searches save edges viaLCAcalculation of two nodes.
		staticLCATree = enum.auto()

		#: Same as staticLCATree but each time a triple has been contracted the "weight tree" is updated dynamically rather than completely new from scratch. Has the fastest update time.
		dynamicLCATree = enum.auto()

		#: Uses staticEnum for the triple generation phase (many queries) and dynamicLCATree during the contraction phase (few updates)
		hybrid = enum.auto()

	Triple : Type = steiner_tree.Triple[ TYPE ]

	class TripleGeneration(enum.Enum):

		"""Choice of triple generation."""

		#: try all possibilities
		exhaustive = enum.auto()

		#: use voronoi regions
		voronoi = enum.auto()

		#: generate triples "on the fly", only usable withWinCalculation::absolute
		ondemand = enum.auto()

	class TripleReduction(enum.Enum):

		"""Switches immediate triple dropping."""

		#: removes triples as soon as their gain is known to be non positive
		on = enum.auto()

		#: keeps triples all the time
		off = enum.auto()

	class WinCalculation(enum.Enum):

		"""Choice of objective function."""

		#: win=gain-cost
		absolute = enum.auto()

		#: win=gain/cost
		relative = enum.auto()

	def __init__(self, wc : WinCalculation = WinCalculation.absolute, tg : TripleGeneration = TripleGeneration.voronoi, sc : SaveCalculation = SaveCalculation.hybrid, tr : TripleReduction = TripleReduction.on, _pass : Pass = Pass.multi) -> None:
		...

	def __destruct__(self) -> None:
		...

	def call(self, G : EdgeWeightedGraph[ T ], terminals : List[node], isTerminal : NodeArray[ bool ], finalSteinerTree : EdgeWeightedGraphCopy[ T ]) -> T:
		"""Calls the Steiner tree algorithm for nontrivial cases but handles trivial cases directly."""
		...

	def forceAPSP(self, force : bool = True) -> None:
		"""For the 3-restricted case, it is sufficient to compute an SSSP from every terminal instead of doing a full APSP."""
		...

	def numberOfContractedTriples(self) -> int:
		"""Returns the number of contracted triples."""
		...

	def numberOfGeneratedTriples(self) -> int:
		"""Returns the number of generated triples."""
		...

	def numberOfTripleLookUps(self) -> int:
		"""Returns the number of triple lookups during execution time."""
		...

	@overload
	def _pass(self) -> Pass:
		"""Returns type of pass currently in use."""
		...

	@overload
	def _pass(self, p : Pass) -> None:
		"""Sets type of pass."""
		...

	@overload
	def saveCalculation(self) -> SaveCalculation:
		"""Returns type of save calculation currently in use."""
		...

	@overload
	def saveCalculation(self, sv : SaveCalculation) -> None:
		"""Sets type of save calculation."""
		...

	@overload
	def tripleGeneration(self) -> TripleGeneration:
		"""Returns type of triple generation currently in use."""
		...

	@overload
	def tripleGeneration(self, tg : TripleGeneration) -> None:
		"""Sets type of triple generation."""
		...

	@overload
	def tripleReduction(self) -> TripleReduction:
		"""Returns type of triple reduction currently in use."""
		...

	@overload
	def tripleReduction(self, tr : TripleReduction) -> None:
		"""Sets type of triple reduction."""
		...

	@overload
	def winCalculation(self) -> WinCalculation:
		"""Returns type of gain calculation currently in use."""
		...

	@overload
	def winCalculation(self, wc : WinCalculation) -> None:
		"""Sets type of gain calculation."""
		...

	def calcWin(self, gain : float, cost : T) -> float:
		"""Calculate the win."""
		...

	def computeDistanceMatrix(self) -> None:
		"""Computes the distance matrix for the original graph."""
		...

	def computeSteinerTree(self, G : EdgeWeightedGraph[ T ], terminals : List[node], isTerminal : NodeArray[ bool ], finalSteinerTree : EdgeWeightedGraphCopy[ T ]) -> T:
		"""Builds a minimum Steiner tree given a weighted graph and a list of terminals."""
		...

	def contractTriple(self, triple : Triple[ T ], save : Save[ T ], isNewTerminal : NodeArray[ bool ]) -> None:
		"""Contracts a triple and updates the save data structure."""
		...

	def findBestTripleForCenter(self, center : node, save : Save[ T ], maxTriple : Triple[ T ]) -> bool:
		"""Find the best triple for a given nonterminal center."""
		...

	def generateInitialTerminalSpanningTree(self, steinerTree : EdgeWeightedGraphCopy[ T ]) -> None:
		...

	def generateTriple(self, u : node, v : node, w : node, center : node, minCost : T, save : Save[ T ]) -> None:
		"""Add a found triple to the triples list."""
		...

	@overload
	def generateTriples(self, save : Save[ T ]) -> None:
		"""Generates triples according to the chosen option."""
		...

	@overload
	def generateTriples(self, save : Save[ T ], fcg : steiner_tree.Full3ComponentGeneratorModule[ T ]) -> None:
		"""Generates triples using the given full 3-component generator."""
		...

	def multiPass(self, save : Save[ T ], isNewTerminal : NodeArray[ bool ]) -> None:
		"""Contraction phase for the original version of the algorithm."""
		...

	def onePass(self, save : Save[ T ], isNewTerminal : NodeArray[ bool ]) -> None:
		"""Contraction phase for the one pass heuristic."""
		...

	def tripleOnDemand(self, save : Save[ T ], isNewTerminal : NodeArray[ bool ]) -> None:
		"""Contraction phase for algorithm generating triples on demand."""
		...
