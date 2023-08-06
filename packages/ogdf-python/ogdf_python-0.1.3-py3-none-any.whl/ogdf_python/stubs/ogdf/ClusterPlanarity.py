# file stubs/ogdf/ClusterPlanarity.py generated from classogdf_1_1_cluster_planarity
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
class ClusterPlanarity(ogdf.ClusterPlanarModule):

	"""C-planarity testing via completely connected graph extension."""

	CP_MasterBase : Type = cluster_planarity.CP_MasterBase

	NodePairs : Type = List[NodePair]

	class solmeth(enum.Enum):

		"""Solution method, fallback to old version (allowing all extension edges, based on c-planar subgraph computation) or new direct version (allowing only a reduced set of extension edges for complete connectivity)."""

		Fallback = enum.auto()

		New = enum.auto()

	def __init__(self) -> None:
		"""Construction."""
		...

	def __destruct__(self) -> None:
		...

	def getHeurTime(self) -> float:
		...

	def getLPSolverTime(self) -> float:
		...

	def getLPTime(self) -> float:
		...

	def getNumBCs(self) -> int:
		"""Returns number of generated LPs."""
		...

	def getNumCCons(self) -> int:
		"""Returns number of connectivity constraints added during computation."""
		...

	def getNumKCons(self) -> int:
		"""Returns number of Kuratowski constraints added during computation."""
		...

	def getNumLPs(self) -> int:
		"""Returns number of optimized LPs (only LP-relaxations)"""
		...

	def getNumSubSelected(self) -> int:
		"""Returns number of subproblems selected by ABACUS."""
		...

	def getNumVars(self) -> int:
		"""Returns number of global variables. Todo: Real number from ABACUS."""
		...

	def getOptStatus(self) -> abacus.Master.STATUS:
		...

	def getSeparationTime(self) -> float:
		...

	def getTotalTime(self) -> float:
		...

	def getTotalWTime(self) -> float:
		...

	@overload
	def isClusterPlanar(self, CG : ClusterGraph) -> bool:
		"""Returns c-planarity status ofCG."""
		...

	@overload
	def isClusterPlanar(self, CG : ClusterGraph, addedEdges : NodePairs) -> bool:
		"""Computes a set of edges that augments the subgraph to be completely connected and returns c-planarity status and edge set."""
		...

	def setBranchingGap(self, d : float) -> None:
		...

	def setHeuristicBound(self, d : float) -> None:
		...

	def setHeuristicLevel(self, i : int) -> None:
		...

	def setHeuristicRuns(self, i : int) -> None:
		...

	def setLowerRounding(self, d : float) -> None:
		...

	def setNumAddVariables(self, n : int) -> None:
		...

	def setNumberOfKuraIterations(self, i : int) -> None:
		...

	def setNumberOfPermutations(self, i : int) -> None:
		...

	def setNumberOfSubDivisions(self, i : int) -> None:
		...

	def setNumberOfSupportGraphs(self, i : int) -> None:
		...

	def setPerturbation(self, b : bool) -> None:
		...

	def setPortaOutput(self, b : bool) -> None:
		...

	def setPricing(self, b : bool) -> None:
		...

	def setStrongConstraintViolation(self, d : float) -> None:
		...

	def setStrongVariableViolation(self, d : float) -> None:
		...

	def setTimeLimit(self, s : str) -> None:
		...

	def setUpperRounding(self, d : float) -> None:
		...

	def solutionMethod(self) -> solmeth:
		...

	def useDefaultCutPool(self) -> bool:
		"""Use default abacus master cut pool or dedicated connectivity and kuratowski cut pools."""
		...

	def writeFeasible(self, filename : str, master : CP_MasterBase, status : abacus.Master.STATUS) -> None:
		"""Writes feasible solutions as a file in PORTA format."""
		...

	@overload
	def doTest(self, CG : ClusterGraph) -> bool:
		"""Performs a c-planarity test on CG."""
		...

	@overload
	def doTest(self, G : ClusterGraph, addedEdges : NodePairs) -> bool:
		...

	def getBottomUpClusterList(self, c : cluster, theList : List[cluster]) -> None:
		"""Stores clusters in subtree at c in bottom up order in theList."""
		...

	def getDoubleTime(self, act : Stopwatch) -> float:
		...
