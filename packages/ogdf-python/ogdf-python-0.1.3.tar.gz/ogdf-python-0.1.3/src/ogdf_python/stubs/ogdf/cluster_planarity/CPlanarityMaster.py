# file stubs/ogdf/cluster_planarity/CPlanarityMaster.py generated from classogdf_1_1cluster__planarity_1_1_c_planarity_master
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
class CPlanarityMaster(ogdf.cluster_planarity.CP_MasterBase):

	def __init__(self, C : ClusterGraph, heuristicLevel : int = 0, heuristicRuns : int = 2, heuristicOEdgeBound : float = 0.3, heuristicNPermLists : int = 5, kuratowskiIterations : int = 3, subdivisions : int = 10, kSupportGraphs : int = 3, kuratowskiHigh : float = 0.75, kuratowskiLow : float = 0.3, perturbation : bool = False, branchingGap : float = 0.4, time : str = "00:20:00") -> None:
		...

	def __destruct__(self) -> None:
		"""Destruction."""
		...

	def branchingOEdgeSelectGap(self) -> float:
		...

	def firstSub(self) -> abacus.Sub:
		"""Should return a pointer to the first subproblem of the optimization, i.e., the root node of the enumeration tree."""
		...

	def getClusterGraph(self) -> ClusterGraph:
		...

	@overload
	def getClusterNodes(self, c : cluster) -> List[node]:
		"""Returns reference to cluster nodes member list forc."""
		...

	@overload
	def getClusterNodes(self, c : cluster, nodeList : List[node]) -> None:
		"""Copies cluster nodes from member list to parameter list. Should be used if node list needs to be altered."""
		...

	def getConnectionOptimalSolutionEdges(self, edges : List[NodePair]) -> None:
		"""Returns nodePairs of connecting optimal solution edges in listedges."""
		...

	def getGraph(self) -> Graph:
		...

	def getHeuristicFractionalBound(self) -> float:
		...

	def getHeuristicLevel(self) -> int:
		...

	def getHeuristicRuns(self) -> int:
		...

	def getKBoundHigh(self) -> float:
		...

	def getKBoundLow(self) -> float:
		...

	def getKIterations(self) -> int:
		...

	def getMPHeuristic(self) -> bool:
		...

	def getNKuratowskiSupportGraphs(self) -> int:
		...

	def getNSubdivisions(self) -> int:
		...

	def getNumAddVariables(self) -> int:
		...

	def getNumInactiveVars(self) -> int:
		...

	def getStdConstraintsFileName(self) -> str:
		"""The name of the file that contains the standard, i.e., non-cut, constraints (may be deleted by ABACUS and shouldn't be stored twice)"""
		...

	def getStrongConstraintViolation(self) -> float:
		...

	def getStrongVariableViolation(self) -> float:
		...

	def heuristicLevel(self, level : int) -> None:
		...

	def nMaxVars(self) -> int:
		...

	def numberOfHeuristicPermutationLists(self) -> int:
		...

	def perturbation(self) -> bool:
		...

	def searchSpaceGraph(self) -> GraphCopy:
		...

	def setHeuristicFractionalBound(self, b : float) -> None:
		...

	def setHeuristicPermutationLists(self, n : int) -> None:
		...

	def setHeuristicRuns(self, n : int) -> None:
		...

	def setKBoundHigh(self, n : float) -> None:
		...

	def setKBoundLow(self, n : float) -> None:
		...

	def setKIterations(self, n : int) -> None:
		...

	def setMPHeuristic(self, b : bool) -> None:
		"""Switches use of lower bound heuristic."""
		...

	def setNHeuristicRuns(self, n : int) -> None:
		...

	def setNKuratowskiSupportGraphs(self, n : int) -> None:
		...

	def setNSubdivisions(self, n : int) -> None:
		...

	def setNumAddVariables(self, i : int) -> None:
		...

	def setPertubation(self, b : bool) -> None:
		...

	def setSearchSpaceShrinking(self, b : bool) -> None:
		"""Toggles reduction of search space (using only some bag/satchel connections) on/off."""
		...

	def setStrongConstraintViolation(self, d : float) -> None:
		...

	def setStrongVariableViolation(self, d : float) -> None:
		...

	def solutionInducedGraph(self) -> Graph:
		"""Returns the optimal solution induced Clustergraph."""
		...

	def updateBestSubGraph(self, connection : List[NodePair]) -> None:
		"""Updates the "best" Subgraphm_solutionGraphfound so far and fillsconnectionwith."""
		...

	def addExternalConnections(self, c : cluster, connectVars : List[CPlanarEdgeVar]) -> None:
		"""Create variables for external cluster connections in case we search only in the bag-reduced search space."""
		...

	def addInnerConnections(self, c : cluster, connectVars : List[CPlanarEdgeVar]) -> None:
		"""Adds inner cluster connection variables in bag-reduced search space."""
		...

	def createInitialVariables(self, initVars : List[CPlanarEdgeVar]) -> None:
		"""All variables that have to be present at start of optimization are created here. Their number is returned."""
		...

	def goodVar(self, a : node, b : node) -> bool:
		"""Node pair is potential candidate for new edge variable."""
		...

	def heuristicInitialLowerBound(self) -> float:
		...

	def initializeOptimization(self) -> None:
		"""The default implementation ofinitializeOptimization()does nothing."""
		...

	def isCP(self) -> bool:
		"""Derives and returns c-planarity property either directly or indirectly from computation results."""
		...

	def terminateOptimization(self) -> None:
		"""Function that is invoked at the end of the optimization. Does nothing but output inCP_MasterBase."""
		...
