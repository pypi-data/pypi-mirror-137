# file stubs/ogdf/MinSteinerTreeDirectedCut/DirectedCutConstraint.py generated from classogdf_1_1_min_steiner_tree_directed_cut_1_1_directed_cut_constraint
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
class DirectedCutConstraint(abacus.Constraint):

	"""Class for directed cuts (i.e., separated Steiner cuts)"""

	def __init__(self, master : abacus.Master, g : Graph, minSTCut : MinSTCutMaxFlow[ float ], _cutType : MinSTCutMaxFlow[ float ].cutType) -> None:
		...

	def active(self, n : node) -> bool:
		"""returns true iff the node n is separated by this cut"""
		...

	def coeff(self, v : abacus.Variable) -> float:
		"""Returns the coefficient of the variablevin the constraint."""
		...

	def cutedge(self, e : edge) -> bool:
		"""returns true iff the edge is contained in the cut"""
		...

	def equal(self, cv : ConVar) -> bool:
		"""tests if cuts are equal; required method for nonduplpool"""
		...

	def hashKey(self) -> None:
		"""retuns an hashkey for the cut; required method for nonduplpool"""
		...

	def marked(self, n : node) -> bool:
		"""returns status of node n"""
		...

	def name(self) -> str:
		"""return the name of the cut; required method for nonduplpool"""
		...

	def nMarkedNodes(self) -> int:
		"""the number of marked nodes"""
		...
