# file stubs/ogdf/steiner_tree/goemans/CoreEdgeModule.py generated from classogdf_1_1steiner__tree_1_1goemans_1_1_core_edge_module
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
T = TypeVar('T')

class CoreEdgeModule(Generic[T]):

	"""Interface for core edge finder algorithms."""

	def call(self, graph : Graph, terminals : List[node], isInTree : EdgeArray[ bool ]) -> None:
		"""Compute a set of core edges."""
		...
