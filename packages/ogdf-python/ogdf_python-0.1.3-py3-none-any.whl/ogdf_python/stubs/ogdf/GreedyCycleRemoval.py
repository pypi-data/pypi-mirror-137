# file stubs/ogdf/GreedyCycleRemoval.py generated from classogdf_1_1_greedy_cycle_removal
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
class GreedyCycleRemoval(ogdf.AcyclicSubgraphModule):

	"""Greedy algorithm for computing a maximal acyclic subgraph."""

	def __init__(self) -> None:
		...

	def call(self, G : Graph, arcSet : List[edge]) -> None:
		"""Computes the set of edgesarcSet, which have to be deleted in the acyclic subgraph."""
		...
