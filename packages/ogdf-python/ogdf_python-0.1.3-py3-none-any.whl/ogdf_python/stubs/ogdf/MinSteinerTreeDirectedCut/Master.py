# file stubs/ogdf/MinSteinerTreeDirectedCut/Master.py generated from classogdf_1_1_min_steiner_tree_directed_cut_1_1_master
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
class Master(abacus.Master, ogdf.Logger):

	"""Master problem of Steiner tree branch&cut algorithm"""

	def __init__(self, wG : EdgeWeightedGraph[ T ], terminals : List[node], isTerminal : NodeArray[ bool ], eps : float, relaxed : bool = False) -> None:
		"""Constructor of the master problem."""
		...

	def __destruct__(self) -> None:
		"""destructor"""
		...

	def bestSolution(self) -> float:
		"""the best found solution"""
		...

	def callPrimalHeuristic(self) -> bool:
		"""parameter: call primal heuristic yes/no"""
		...

	def callPrimalHeuristicStrategy(self) -> int:
		"""strategy for calling primal heuristic (PH)"""
		...

	@overload
	def capacities(self) -> EdgeArray[ float ]:
		"""edge costs"""
		...

	@overload
	def capacities(self, e : edge) -> float:
		"""costs for edge e"""
		...

	def checkSetMaxPoolSize(self) -> None:
		"""checks if current pool size is maximum and sets it if necessary"""
		...

	def computeBackCuts(self) -> bool:
		"""parameter: back cut computation"""
		...

	def computeNestedCuts(self) -> bool:
		"""parameter: nested cut computation"""
		...

	def cutPool(self) -> abacus.NonDuplPool[abacus.Constraint,abacus.Variable]:
		"""the non-duplicate cutpool for the separated Steiner cuts"""
		...

	def edgeGToWgPH(self, e : edge) -> edge:
		"""edge mapping m_pGraph -> m_pWeightedGraphPH"""
		...

	def edgeID(self, e : edge) -> int:
		"""edge -> id of lp variable"""
		...

	def edgeIDs(self) -> EdgeArray[  int ]:
		"""lp variable ids of edges"""
		...

	def edgeWgToGPH(self, e : edge) -> edge:
		"""edge mapping m_pWeightedGraphPH -> m_pGraph"""
		...

	def firstSub(self) -> abacus.Sub:
		"""generates the first subproblem"""
		...

	def getEdge(self, i : int) -> edge:
		"""id -> edge"""
		...

	def getMaxFlowModule(self) -> MaxFlowModule[ float ]:
		"""Get the maximum flow module used by separation algorithm."""
		...

	def getNode(self, i : int) -> node:
		"""id -> node"""
		...

	def getPrimalHeuristic(self) -> std.unique_ptr[MinSteinerTreeModule[ float ] ]:
		"""the primal heuristic module"""
		...

	def getVar(self, e : edge) -> EdgeVariable:
		"""returns the variable assigned to edge e"""
		...

	def getVarTwin(self, e : edge) -> EdgeVariable:
		"""returns the variable assigned to the twin of edge e"""
		...

	def graph(self) -> Graph:
		"""the directed graph, i.e., the bidirection of the input graph"""
		...

	@overload
	def incNrCutsTotal(self) -> None:
		"""increases the number of separated directed cuts by 1"""
		...

	@overload
	def incNrCutsTotal(self, val : int) -> None:
		"""increases the number of separated directed cuts"""
		...

	def isSolutionEdge(self, e : edge) -> bool:
		"""returns true iff original edge is contained in optimum solution"""
		...

	@overload
	def isTerminal(self) -> NodeArray[ bool ]:
		"""boolean array of terminal status"""
		...

	@overload
	def isTerminal(self, n : node) -> bool:
		"""true if n is a terminal"""
		...

	def isTerminalPH(self) -> NodeArray[ bool ]:
		"""terminal yes/no (in m_pWeightedGraphPH)"""
		...

	def maxNrAddedCuttingPlanes(self) -> int:
		"""maximum nr of cutting planes"""
		...

	def maxPoolSize(self) -> int:
		"""the maximum pool size during the algorithm"""
		...

	def minCardinalityCuts(self) -> bool:
		"""parameter: compute minimum cardinality cuts"""
		...

	def nEdges(self) -> int:
		"""returns the number of edges"""
		...

	def nEdgesU(self) -> int:
		"""returns number of undirected edges, i.e.,nEdges()/2"""
		...

	def nNodes(self) -> int:
		"""number of nodes of the graph"""
		...

	def nodeID(self, n : node) -> int:
		"""npde -> id of lp variable"""
		...

	def nodeIDs(self) -> NodeArray[  int ]:
		"""lp variable ids of nodes"""
		...

	def nodes(self) -> node:
		"""nodes of the graph"""
		...

	def nrCutsTotal(self) -> int:
		"""total number of separated directed cuts"""
		...

	def nTerminals(self) -> int:
		"""number of terminals"""
		...

	def poolSizeInit(self) -> int:
		"""initial pool size"""
		...

	def primalHeuristicTimer(self) -> StopwatchWallClock:
		"""timer for primal heuristics"""
		...

	def relaxed(self) -> bool:
		"""solve relaxed LP or ILP"""
		...

	def rootNode(self) -> node:
		"""the designated root node (special terminal)"""
		...

	def rootNodePH(self) -> node:
		"""root node (in m_pWeightedGraphPH)"""
		...

	def saturationStrategy(self) -> int:
		"""strategy for saturating edges during separation; Only relevant for nested cuts"""
		...

	def separationStrategy(self) -> int:
		"""strategy for separating directed Steiner cuts; Only relevant for nested cuts"""
		...

	def separationTimer(self) -> StopwatchWallClock:
		"""timer for separation"""
		...

	def setConfigFile(self, filename : str) -> None:
		"""Set the config file to use that overrides all other settings."""
		...

	def setMaxFlowModule(self, module : MaxFlowModule[ float ]) -> None:
		"""Set the maximum flow module to be used for separation."""
		...

	def setMaxNumberAddedCuttingPlanes(self, b : int) -> None:
		"""Set maximum number of added cutting planes per iteration."""
		...

	def setNIterRoot(self, val : int) -> None:
		"""nr of iterations in the root node"""
		...

	def setPoolSizeInitFactor(self, b : int) -> None:
		"""Set factor for the initial size of the cutting pool."""
		...

	def setPrimalHeuristic(self, pMinSteinerTreeModule : MinSteinerTreeModule[ float ]) -> None:
		"""Set the module option for the primal heuristic."""
		...

	def setPrimalHeuristicCallStrategy(self, b : int) -> None:
		"""Set primal heuristic call strategy."""
		...

	def setRelaxedSolValue(self, val : float) -> None:
		"""solution value of the root"""
		...

	def setSaturationStrategy(self, b : int) -> None:
		"""Set saturation strategy for nested cuts."""
		...

	def setSeparationStrategy(self, b : int) -> None:
		"""Set separation strategy for nested cuts."""
		...

	def shuffleTerminals(self) -> bool:
		"""shuffle ordering of terminals before each separation routine"""
		...

	def solutionValue(self) -> float:
		"""solution value after solving the problem, i.e., returns final primal bound"""
		...

	def terminal(self, i : int) -> node:
		"""get terminal with index i"""
		...

	def terminalListPH(self) -> List[node]:
		"""list of terminals (in m_pWeightedGraphPH)"""
		...

	def terminals(self) -> node:
		"""terminals in an array"""
		...

	def timerMinSTCut(self) -> StopwatchWallClock:
		"""timer for minimum st-cut computations. Measures updates + algorithm"""
		...

	def twin(self, e : edge) -> edge:
		"""the twin edge, i.e. twin[(u,v)] = (v,u)"""
		...

	def twins(self) -> EdgeArray[edge]:
		...

	def updateBestSolution(self, values : float) -> None:
		"""updates best found solution"""
		...

	def updateBestSolutionByEdges(self, sol : List[edge]) -> None:
		"""updates best found solution by list of edges"""
		...

	def useBackCuts(self, b : bool) -> None:
		"""Switch computation of back-cuts on or off."""
		...

	def useDegreeConstraints(self, b : bool) -> None:
		"""Switch usage of degree constraints (like indeg <= 1) on or off."""
		...

	def useFlowBalanceConstraints(self, b : bool) -> None:
		"""Switch usage of flow balance constraints on or off."""
		...

	def useGSEC2Constraints(self, b : bool) -> None:
		"""Switch usage of constraints x_uv + x_vu <= 1 on or off."""
		...

	def useIndegreeEdgeConstraints(self, b : bool) -> None:
		"""Switch usage of indegree edge constraints (indeg(v) >= outgoing edge(v,x) for all x) on or off."""
		...

	def useMinCardinalityCuts(self, b : bool) -> None:
		"""Switch usage of the cardinality heuristic (minimum-cardinality cuts) on or off."""
		...

	def useNestedCuts(self, b : bool) -> None:
		"""Switch computation of nested cuts on or off."""
		...

	def useTerminalShuffle(self, b : bool) -> None:
		"""Switch terminal shuffling before separation on or off."""
		...

	def weightedGraphPH(self) -> EdgeWeightedGraph[ float ]:
		...

	def initializeOptimization(self) -> None:
		"""insert variables and base constraints"""
		...

	def initializeParameters(self) -> None:
		"""read/set parameters from file"""
		...

	def terminateOptimization(self) -> None:
		"""store solution inEdgeArray"""
		...
