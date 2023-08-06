# file stubs/ogdf/steiner_tree/FullComponentGeneratorDreyfusWagnerWithoutMatrix/__init__.py generated from classogdf_1_1steiner__tree_1_1_full_component_generator_dreyfus_wagner_without_matrix
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
T = TypeVar('T')

class FullComponentGeneratorDreyfusWagnerWithoutMatrix(Generic[T]):

	"""A generator for restricted full components (for Steiner tree approximations) based on the Dreyfus-Wagner algorithm that does not need a precomputed all-pair-shortest-paths matrix because single-source-shortest-path are used within."""

	def __init__(self, G : EdgeWeightedGraph[ T ], terminals : List[node], isTerminal : NodeArray[ bool ]) -> None:
		"""The constructor."""
		...

	def call(self, restricted : int) -> None:
		...

	def getSteinerTreeFor(self, terminals : List[node], tree : EdgeWeightedGraphCopy[ T ]) -> T:
		"""Constructs a Steiner tree for the given set of terminals if it is valid, otherwise an empty tree is returned."""
		...

	def isValidComponent(self, tree : EdgeWeightedGraphCopy[ T ]) -> bool:
		"""Checks if a giventreeis a valid full component."""
		...
