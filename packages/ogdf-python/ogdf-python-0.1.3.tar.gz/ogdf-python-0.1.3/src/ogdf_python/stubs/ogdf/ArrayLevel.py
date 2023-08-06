# file stubs/ogdf/ArrayLevel.py generated from classogdf_1_1_array_level
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
class ArrayLevel(ogdf.LevelBase):

	"""The simple implementation ofLevelBaseinterface."""

	@overload
	def __init__(self, nodes : Array[node]) -> None:
		...

	@overload
	def __init__(self, size : int) -> None:
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
