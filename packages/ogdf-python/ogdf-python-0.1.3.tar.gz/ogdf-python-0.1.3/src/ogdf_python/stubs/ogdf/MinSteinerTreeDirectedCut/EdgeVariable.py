# file stubs/ogdf/MinSteinerTreeDirectedCut/EdgeVariable.py generated from classogdf_1_1_min_steiner_tree_directed_cut_1_1_edge_variable
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
class EdgeVariable(abacus.Variable):

	"""Variable for directed edges."""

	def __init__(self, master : abacus.Master, id : int, e : edge, coeff : float, lb : float = 0.0, ub : float = 1.0, vartype : abacus.VarType.TYPE = abacus.VarType.Binary) -> None:
		...

	def coefficient(self) -> float:
		"""objective function coefficient"""
		...

	def id(self) -> int:
		"""id of the edge (variable)"""
		...

	def source(self) -> node:
		"""source node"""
		...

	def target(self) -> node:
		"""target node"""
		...

	def theEdge(self) -> edge:
		"""the associated edge"""
		...
