# file stubs/ogdf/cluster_planarity/MaxPlanarEdgesConstraint.py generated from classogdf_1_1cluster__planarity_1_1_max_planar_edges_constraint
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
class MaxPlanarEdgesConstraint(abacus.Constraint):

	@overload
	def __init__(self, master : abacus.Master, edgeBound : int) -> None:
		...

	@overload
	def __init__(self, master : abacus.Master, edgeBound : int, edges : List[NodePair]) -> None:
		...

	def __destruct__(self) -> None:
		...

	def coeff(self, v : abacus.Variable) -> float:
		"""Returns the coefficient of the variablevin the constraint."""
		...
