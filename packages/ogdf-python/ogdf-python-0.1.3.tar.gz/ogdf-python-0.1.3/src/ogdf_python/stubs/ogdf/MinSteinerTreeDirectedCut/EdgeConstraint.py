# file stubs/ogdf/MinSteinerTreeDirectedCut/EdgeConstraint.py generated from classogdf_1_1_min_steiner_tree_directed_cut_1_1_edge_constraint
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
class EdgeConstraint(abacus.Constraint):

	"""Constraint for edges, e.g., subtour elimination constraints of size 2 ((G)SEC2)"""

	def __init__(self, master : abacus.Master, e1 : edge, e2 : edge, factor : int = 1.0, sense : abacus.CSense.SENSE = abacus.CSense.Less, rhs : float = 1.0) -> None:
		...

	def coeff(self, v : abacus.Variable) -> float:
		"""coefficient of variable in constraint"""
		...
