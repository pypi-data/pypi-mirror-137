# file stubs/ogdf/AStarSearch.py generated from classogdf_1_1_a_star_search
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
T = TypeVar('T')

class AStarSearch(Generic[T]):

	"""A-Star informed search algorithm."""

	def __init__(self, directed : bool = False, maxGap : float = 1, et : EpsilonTest = EpsilonTest()) -> None:
		"""Initializes a new A* search algorithm."""
		...

	def call(self, graph : Graph, cost : EdgeArray[ T ], source : node, target : node, predecessor : NodeArray[edge], heuristic : Callable = print) -> T:
		"""Computes the shortests path betweensourceandtarget."""
		...
