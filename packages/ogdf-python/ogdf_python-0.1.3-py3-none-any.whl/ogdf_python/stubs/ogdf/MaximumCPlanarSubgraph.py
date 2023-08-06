# file stubs/ogdf/MaximumCPlanarSubgraph.py generated from classogdf_1_1_maximum_c_planar_subgraph
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
class MaximumCPlanarSubgraph(ogdf.CPlanarSubgraphModule):

	"""Exact computation of a maximum c-planar subgraph."""

	MaxCPlanarMaster : Type = cluster_planarity.MaxCPlanarMaster

	NodePairs : Type = List[NodePair]

	def __init__(self) -> None:
		"""Construction."""
		...

	def __destruct__(self) -> None:
		...

	def callAndConnect(self, G : ClusterGraph, pCost : EdgeArray[ float ], delEdges : List[edge], addedEdges : NodePairs) -> ReturnType:
		"""Computes set of edges delEdges, which have to be deleted in order to get a c-planar subgraph and also returns a set of edges that augments the subgraph to be completely connected. For pure c-planarity testing, the computation can be sped up by setting setCheckCPlanar(2). Then, in case G is not c-planar, the list of deleted edges does not need to correspond to a valid solution, it just indicates the result."""
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

	def getSeparationTime(self) -> float:
		...

	def getTotalTime(self) -> float:
		...

	def getTotalWTime(self) -> float:
		...

	def setBranchingGap(self, d : float) -> None:
		...

	def setCheckCPlanar(self, b : bool) -> None:
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

	@overload
	def setTimeLimit(self, milliSec : std.chrono.milliseconds) -> None:
		...

	@overload
	def setTimeLimit(self, s : str) -> None:
		...

	def setUpperRounding(self, d : float) -> None:
		...

	def useDefaultCutPool(self) -> bool:
		"""Use default abacus master cut pool or dedicated connectivity and kuratowski cut pools."""
		...

	def writeFeasible(self, filename : str, master : MaxCPlanarMaster, status : abacus.Master.STATUS) -> None:
		"""Writes feasible solutions as a file in PORTA format."""
		...

	@overload
	def doCall(self, G : ClusterGraph, pCost : EdgeArray[ float ], delEdges : List[edge]) -> ReturnType:
		"""Computes a maximum c-planar subgraph, returns the set of edges that have to be deleted in delEdges if delEdges is empty on return, the clustered graph G is c-planar."""
		...

	@overload
	def doCall(self, G : ClusterGraph, pCost : EdgeArray[ float ], delEdges : List[edge], addedEdges : NodePairs) -> ReturnType:
		...

	def getBottomUpClusterList(self, c : cluster, theList : List[cluster]) -> None:
		"""Stores clusters in subtree at c in bottom up order in theList."""
		...

	def getDoubleTime(self, act : Stopwatch) -> float:
		...
