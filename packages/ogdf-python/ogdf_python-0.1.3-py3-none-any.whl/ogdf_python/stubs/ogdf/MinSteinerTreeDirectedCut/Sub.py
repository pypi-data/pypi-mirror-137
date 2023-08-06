# file stubs/ogdf/MinSteinerTreeDirectedCut/Sub.py generated from classogdf_1_1_min_steiner_tree_directed_cut_1_1_sub
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
class Sub(abacus.Sub):

	"""Subproblem of Steiner tree algorithm."""

	@overload
	def __init__(self, master : abacus.Master) -> None:
		"""Constructor for the root problem of the b&b tree."""
		...

	@overload
	def __init__(self, master : abacus.Master, father : abacus.Sub, branchRule : abacus.BranchRule) -> None:
		"""Constructor for non-root problems of the b&b tree."""
		...

	def __destruct__(self) -> None:
		"""The destructor only deletes the sons of the node."""
		...

	def feasible(self) -> bool:
		"""checks if the current solution is feasible, i.e., callsmySeparate()"""
		...

	def myImprove(self) -> None:
		"""primal heuristic procedure"""
		...

	def mySeparate(self) -> int:
		"""separation procedure"""
		...

	def separate(self) -> int:
		"""callsmySeparate()if mySeparate wasn't called in another procedure"""
		...
