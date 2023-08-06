# file stubs/ogdf/steiner_tree/SaveEnum.py generated from classogdf_1_1steiner__tree_1_1_save_enum
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
T = TypeVar('T')

class SaveEnum(ogdf.steiner_tree.Save[ T ], Generic[T]):

	"""This class computes save edges recursively and stores for every node pair their save edge in aHashArray."""

	def __init__(self, steinerTree : EdgeWeightedGraphCopy[ T ]) -> None:
		"""Initializes the data structures and calculates a MST of the given complete terminal graph."""
		...

	def __destruct__(self) -> None:
		...

	def gain(self, u : node, v : node, w : node) -> T:
		"""Returns the gain (sum of the save edges) of a node triple by an table lookup."""
		...

	def rebuild(self) -> None:
		"""Rebuild the lookup table (necessary if the tree has changed)"""
		...

	def saveEdge(self, u : node, v : node) -> edge:
		"""Determines the save edge between two nodes by a table lookup."""
		...

	def saveWeight(self, u : node, v : node) -> T:
		"""Determines the weight of the save edge between two nodes by a table lookup."""
		...

	def update(self, t : Triple[ T ]) -> None:
		"""Updates the weighted tree data structure given a contracted triple."""
		...

	def build(self) -> None:
		"""Build the lookup table."""
		...

	def buildRecursively(self, hidden : EdgeArray[ bool ], u : node, processedNodes : List[node]) -> None:
		"""Builds the lookup table for the save edges recursively."""
		...
