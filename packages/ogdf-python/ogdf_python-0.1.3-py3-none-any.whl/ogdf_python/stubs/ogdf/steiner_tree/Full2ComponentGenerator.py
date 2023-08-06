# file stubs/ogdf/steiner_tree/Full2ComponentGenerator.py generated from classogdf_1_1steiner__tree_1_1_full2_component_generator
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
T = TypeVar('T')

class Full2ComponentGenerator(Generic[T]):

	"""Trivial full 2-component generation by lookups of shortest paths between terminal pairs."""

	def call(self, G : EdgeWeightedGraph[ T ], terminals : List[node], distance : NodeArray[NodeArray[ T ]], pred : NodeArray[NodeArray[edge]], generateFunction : Callable) -> None:
		"""Generate full 2-components and callgenerateFunctionfor each full 2-component."""
		...
