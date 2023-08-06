# file stubs/ogdf/MinSteinerTreeDirectedCut/DegreeEdgeConstraint.py generated from classogdf_1_1_min_steiner_tree_directed_cut_1_1_degree_edge_constraint
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
class DegreeEdgeConstraint(abacus.Constraint):

	"""Constraint for relating the indegree and one outgoing edge of a node."""

	def __init__(self, master : abacus.Master, e : edge, coeffIn : float, coeffEdge : float, sense : abacus.CSense.SENSE, rhs : float) -> None:
		...

	def coeff(self, v : abacus.Variable) -> float:
		"""coefficient of variable in constraint"""
		...

	def theEdge(self) -> edge:
		"""the associated edge"""
		...
