# file stubs/ogdf/steiner_tree/SaveDynamic.py generated from classogdf_1_1steiner__tree_1_1_save_dynamic
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
T = TypeVar('T')

class SaveDynamic(ogdf.steiner_tree.Save[ T ], Generic[T]):

	"""Dynamically updatable weighted Tree for determining save edges viaLCAcomputation."""

	def __init__(self, steinerTree : EdgeWeightedGraphCopy[ T ]) -> None:
		"""Builds a weighted binary tree based on the given terminal spanning tree."""
		...

	def __destruct__(self) -> None:
		...

	def gain(self, u : node, v : node, w : node) -> T:
		"""Returns the gain (sum of save edge costs) of the given triple, calculated by anLCAquery."""
		...

	def saveEdge(self, u : node, v : node) -> edge:
		"""Determines the save edge between two nodes by aLCAquery."""
		...

	def saveWeight(self, u : node, v : node) -> T:
		"""Determines the weight of the save edge between two nodes by aLCAquery."""
		...

	def update(self, t : Triple[ T ]) -> None:
		"""Updates the weighted tree data structure given a contracted triple."""
		...

	def lca(self, u : node, v : node) -> node:
		"""Returns the node in m_tree that is theLCAof two nodes."""
		...

	@overload
	def weight(self, e : edge) -> T:
		"""Returns the weight of an edge in the terminal tree or 0."""
		...

	@overload
	def weight(self, v : node) -> T:
		"""Returns the associated weight of a node v in m_tree, or 0 if it is not associated."""
		...
