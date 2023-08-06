# file stubs/ogdf/LevelBase.py generated from classogdf_1_1_level_base
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
class LevelBase(object):

	"""Representation of levels in hierarchies."""

	def __destruct__(self) -> None:
		...

	def high(self) -> int:
		"""Returns the maximal array index (=size()-1)."""
		...

	@overload
	def __getitem__(self, i : int) -> node:
		"""Returns the node at positioni."""
		...

	@overload
	def __getitem__(self, i : int) -> node:
		"""Returns the node at positioni."""
		...

	def size(self) -> int:
		"""Returns the number of nodes on this level."""
		...
