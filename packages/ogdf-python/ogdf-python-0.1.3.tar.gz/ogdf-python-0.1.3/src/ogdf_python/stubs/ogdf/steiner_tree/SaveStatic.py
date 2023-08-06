# file stubs/ogdf/steiner_tree/SaveStatic.py generated from classogdf_1_1steiner__tree_1_1_save_static
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
T = TypeVar('T')

class SaveStatic(ogdf.steiner_tree.Save[ T ], Generic[T]):

	"""This class behaves basically the same asSaveDynamicexcept that the update of the weighted graph is not done dynamically here."""

	def __init__(self, steinerTree : EdgeWeightedGraphCopy[ T ]) -> None:
		...

	def __destruct__(self) -> None:
		...

	def gain(self, u : node, v : node, w : node) -> T:
		"""Returns the gain (sum of the save edges) of a node triple by anLCAquery."""
		...

	def lca(self, u : node, v : node) -> node:
		"""Returns the node corresponding to theLCAbetween two given nodes."""
		...

	def rebuild(self) -> None:
		"""Rebuild the data structure (necessary if the tree has changed)"""
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
