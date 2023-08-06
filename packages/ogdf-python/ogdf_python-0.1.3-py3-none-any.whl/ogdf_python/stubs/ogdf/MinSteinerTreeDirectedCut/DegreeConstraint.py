# file stubs/ogdf/MinSteinerTreeDirectedCut/DegreeConstraint.py generated from classogdf_1_1_min_steiner_tree_directed_cut_1_1_degree_constraint
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
class DegreeConstraint(abacus.Constraint):

	"""Constraint for nodes, e.g., in/outdegree stuff."""

	def __init__(self, master : abacus.Master, n : node, coeffIn : float, coeffOut : float, sense : abacus.CSense.SENSE, rhs : float) -> None:
		...

	def coeff(self, v : abacus.Variable) -> float:
		"""coefficient of variable in constraint"""
		...

	def theNode(self) -> node:
		"""the associated node"""
		...
