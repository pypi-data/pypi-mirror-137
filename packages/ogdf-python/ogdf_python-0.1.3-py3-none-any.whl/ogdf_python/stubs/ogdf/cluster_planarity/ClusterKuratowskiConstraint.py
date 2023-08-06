# file stubs/ogdf/cluster_planarity/ClusterKuratowskiConstraint.py generated from classogdf_1_1cluster__planarity_1_1_cluster_kuratowski_constraint
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
class ClusterKuratowskiConstraint(abacus.Constraint):

	def __init__(self, master : abacus.Master, nEdges : int, ks : SListPure[NodePair]) -> None:
		...

	def __destruct__(self) -> None:
		...

	def coeff(self, v : abacus.Variable) -> float:
		"""Returns the coefficient of the variablevin the constraint."""
		...

	def printMe(self, out : std.ostream) -> None:
		...
