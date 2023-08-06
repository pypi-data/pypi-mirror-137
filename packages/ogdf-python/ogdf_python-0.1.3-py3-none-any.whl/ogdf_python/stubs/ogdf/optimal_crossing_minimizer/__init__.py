# file stubs/ogdf/optimal_crossing_minimizer/__init__.py generated from namespaceogdf_1_1optimal__crossing__minimizer
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
class optimal_crossing_minimizer(object):

	class BranchingMode(enum.Enum):

		Traditional = enum.auto()

		CompleteOdd = enum.auto()

	class GraphHint(enum.Enum):

		_None = enum.auto()

		Complete = enum.auto()

		CompleteBipartite = enum.auto()

		#: only used inOrderedOptimalCrossingMinimizer
		Hypercube = enum.auto()

		#: only used inOrderedOptimalCrossingMinimizer
		ToroidalGrid = enum.auto()

		#: only used inOrderedOptimalCrossingMinimizer
		Petersen = enum.auto()

	class HintEffects(enum.Enum):

		KuratowskisMinusOne = enum.auto()

		AllSubKuratowskis = enum.auto()

		EdgeOrder = enum.auto()

		NodeOrder = enum.auto()

		IterativeLowerBound = enum.auto()

		HighKuratowskiCutsStatic = enum.auto()

		ExpensiveKuratowski = enum.auto()

		#: only used inOrderedOptimalCrossingMinimizer
		HypercubeMinusOne = enum.auto()

		#: only used inOrderedOptimalCrossingMinimizer
		ToroidalGridMinusOne = enum.auto()

		#: only used inOrderedOptimalCrossingMinimizer
		Simplicity = enum.auto()

	class PricingInit(enum.Enum):

		NoPricing = enum.auto()

		#: generate one segment per edge, any other number will generate up to as many segments per edge
		Normal = enum.auto()

	class PricingMode(enum.Enum):

		Reasonable = enum.auto()

		Plenty = enum.auto()

		Few = enum.auto()

		#: only used inOptimalCrossingMinimizer
		Greedy = enum.auto()

		#: only used inOptimalCrossingMinimizer
		Homogenous = enum.auto()

	class SeparationMode(enum.Enum):

		Simple = enum.auto()

		BoyerMyrvold = enum.auto()

	class SolutionSource(enum.Enum):

		Trivial = enum.auto()

		ILP = enum.auto()

		ILPHeuristic = enum.auto()

		Heuristic = enum.auto()

		Kn = enum.auto()

		Knm = enum.auto()

		NoSolution = enum.auto()

	@overload
	def __and__(self, lhs : SeparationMode, rhs : SeparationMode) -> int:
		...

	@overload
	def __and__(self, lhs : int, rhs : HintEffects) -> int:
		...

	@overload
	def __and__(self, lhs : int, rhs : SeparationMode) -> int:
		...

	@overload
	def __lshift__(self, os : std.ostream, obj : BranchingMode) -> std.ostream:
		...

	@overload
	def __lshift__(self, os : std.ostream, obj : GraphHint) -> std.ostream:
		...

	@overload
	def __lshift__(self, os : std.ostream, obj : HintEffects) -> std.ostream:
		...

	@overload
	def __lshift__(self, os : std.ostream, p : optimal_crossing_minimizer.BoyerMyrvoldSeparationParams) -> std.ostream:
		...

	@overload
	def __lshift__(self, os : std.ostream, p : optimal_crossing_minimizer.SimpleSeparationParams) -> std.ostream:
		...

	@overload
	def __lshift__(self, os : std.ostream, obj : PricingInit) -> std.ostream:
		...

	@overload
	def __lshift__(self, os : std.ostream, obj : PricingMode) -> std.ostream:
		...

	@overload
	def __lshift__(self, os : std.ostream, obj : SolutionSource) -> std.ostream:
		...

	@overload
	def __or__(self, lhs : HintEffects, rhs : HintEffects) -> int:
		...

	@overload
	def __or__(self, lhs : int, rhs : HintEffects) -> int:
		...
