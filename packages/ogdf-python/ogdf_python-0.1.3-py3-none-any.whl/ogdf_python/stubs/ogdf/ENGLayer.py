# file stubs/ogdf/ENGLayer.py generated from classogdf_1_1_e_n_g_layer
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
class ENGLayer(object):

	"""Represents layer in an extended nesting graph."""

	def __init__(self) -> None:
		...

	def __destruct__(self) -> None:
		...

	def permute(self) -> None:
		...

	def removeAuxNodes(self) -> None:
		...

	def restore(self) -> None:
		...

	@overload
	def root(self) -> LHTreeNode:
		...

	@overload
	def root(self) -> LHTreeNode:
		...

	def setRoot(self, r : LHTreeNode) -> None:
		...

	def simplifyAdjacencies(self) -> None:
		...

	def store(self) -> None:
		...
