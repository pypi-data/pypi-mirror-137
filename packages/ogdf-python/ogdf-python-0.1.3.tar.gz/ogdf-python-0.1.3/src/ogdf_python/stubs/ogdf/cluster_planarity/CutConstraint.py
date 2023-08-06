# file stubs/ogdf/cluster_planarity/CutConstraint.py generated from classogdf_1_1cluster__planarity_1_1_cut_constraint
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
class CutConstraint(ogdf.cluster_planarity.BaseConstraint):

	def __init__(self, master : abacus.Master, sub : abacus.Sub, edges : List[NodePair]) -> None:
		...

	def __destruct__(self) -> None:
		...

	@overload
	def coeff(self, v : abacus.Variable) -> float:
		"""Returns the coefficient of the variablevin the constraint."""
		...

	@overload
	def coeff(self, n : NodePair) -> int:
		...

	@overload
	def coeff(self, n1 : node, n2 : node) -> int:
		...

	def printMe(self, out : std.ostream) -> None:
		...
