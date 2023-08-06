# file stubs/ogdf/cluster_planarity/CPlanaritySub/__init__.py generated from classogdf_1_1cluster__planarity_1_1_c_planarity_sub
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
class CPlanaritySub(abacus.Sub):

	@overload
	def __init__(self, master : abacus.Master) -> None:
		...

	@overload
	def __init__(self, master : abacus.Master, father : abacus.Sub, branchRule : abacus.BranchRule, criticalConstraints : List[abacus.Constraint]) -> None:
		...

	def __destruct__(self) -> None:
		...

	def generateSon(self, rule : abacus.BranchRule) -> abacus.Sub:
		"""Returns a pointer to an object of a problem specific subproblem, which is generated from the current subproblem by branching rulerule."""
		...

	def addPoolCons(self, cons : ArrayBuffer[abacus.Constraint], pool : abacus.StandardPool[abacus.Constraint,abacus.Variable]) -> int:
		"""Adds the given constraints to the given pool."""
		...

	def checkCConnectivity(self, support : GraphCopy) -> bool:
		"""Checks if the cluster induced graphs and their complement are connected in the current solution."""
		...

	def checkCConnectivityOld(self, support : GraphCopy) -> bool:
		...

	def clusterBags(self, CG : ClusterGraph, c : cluster) -> int:
		"""Computes the number of bags within the given clusterc(non recursive) A bag is a set of chunks within the cluster that are connected via subclusters."""
		...

	def feasible(self) -> bool:
		"""Must check the feasibility of a solution of the LP-relaxation."""
		...

	def getRepresentative(self, v : node, parent : NodeArray[node]) -> node:
		"""run through the pointer list parent and return the representative i.e. the node with parent[v] == v"""
		...

	def improve(self, primalValue : float) -> int:
		"""Can be redefined in order to implement primal heuristics for finding feasible solutions."""
		...

	def makeFeasible(self) -> int:
		"""The default implementation ofmakeFeasible()doesnothing."""
		...

	def optimize(self) -> int:
		"""Performs the optimization of the subproblem."""
		...

	def pricing(self) -> int:
		"""Should generate inactive variables which do not price out correctly."""
		...

	def repair(self) -> int:
		...

	def selectBranchingVariable(self, variable : int) -> int:
		"""Chooses a branching variable."""
		...

	def selectBranchingVariableCandidates(self, candidates : ArrayBuffer[  int ]) -> int:
		"""Selects candidates for branching variables."""
		...

	def separate(self) -> int:
		"""Must be redefined in derived classes for the generation of cutting planes."""
		...

	def separateCutPool(self, pool : abacus.StandardPool[abacus.Constraint,abacus.Variable], minViolation : float) -> int:
		...

	def separateReal(self, minViolate : float) -> int:
		"""these functions are mainly reporting to let abacus think everthing is normal."""
		...

	def separateRealO(self, minViolate : float) -> int:
		...

	def solveLp(self) -> int:
		"""Solves the LP-relaxation of the subproblem."""
		...
