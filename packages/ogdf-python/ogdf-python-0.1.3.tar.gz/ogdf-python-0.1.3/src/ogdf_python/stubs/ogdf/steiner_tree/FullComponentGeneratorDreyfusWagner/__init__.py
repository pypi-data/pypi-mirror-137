# file stubs/ogdf/steiner_tree/FullComponentGeneratorDreyfusWagner/__init__.py generated from classogdf_1_1steiner__tree_1_1_full_component_generator_dreyfus_wagner
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
T = TypeVar('T')

class FullComponentGeneratorDreyfusWagner(Generic[T]):

	"""A generator for restricted full components (for Steiner tree approximations) based on the Dreyfus-Wagner algorithm."""

	def __init__(self, G : EdgeWeightedGraph[ T ], terminals : List[node], isTerminal : NodeArray[ bool ], distance : NodeArray[NodeArray[ T ]], pred : NodeArray[NodeArray[edge]]) -> None:
		"""The constructor."""
		...

	def call(self, restricted : int) -> None:
		...

	def getSteinerTreeFor(self, terminals : List[node], tree : EdgeWeightedGraphCopy[ T ]) -> T:
		"""Constructs a Steiner tree for the given set of terminals if it is valid, otherwise an empty tree is returned."""
		...

	def isValidComponent(self, graph : EdgeWeightedGraphCopy[ T ]) -> bool:
		"""Checks if a givengraphis a valid full component."""
		...
