# file stubs/ogdf/steiner_tree/Save.py generated from classogdf_1_1steiner__tree_1_1_save
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
T = TypeVar('T')

class Save(Generic[T]):

	"""This class serves as an interface for different approaches concerning the calculation of save edges."""

	def __init__(self) -> None:
		...

	def __destruct__(self) -> None:
		...

	def gain(self, u : node, v : node, w : node) -> T:
		"""Returns the gain (sum of the save edges) of a node triple."""
		...

	def saveEdge(self, u : node, v : node) -> edge:
		"""Returns the save edge between two nodes."""
		...

	def saveWeight(self, u : node, v : node) -> T:
		"""Returns the weight of the save edge between two nodes."""
		...

	def update(self, t : Triple[ T ]) -> None:
		"""Updates the weighted tree data structure given a contracted triple."""
		...
