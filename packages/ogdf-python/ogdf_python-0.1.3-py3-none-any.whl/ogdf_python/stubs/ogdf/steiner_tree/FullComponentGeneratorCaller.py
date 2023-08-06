# file stubs/ogdf/steiner_tree/FullComponentGeneratorCaller.py generated from classogdf_1_1steiner__tree_1_1_full_component_generator_caller
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
T = TypeVar('T')

class FullComponentGeneratorCaller(Generic[T]):

	def computeDistanceMatrix(self, distance : NodeArray[NodeArray[ T ]], pred : NodeArray[NodeArray[edge]], graph : EdgeWeightedGraph[ T ], terminals : List[node], isTerminal : NodeArray[ bool ], restricted : int) -> None:
		"""Computes distance and predecessor matrix."""
		...
