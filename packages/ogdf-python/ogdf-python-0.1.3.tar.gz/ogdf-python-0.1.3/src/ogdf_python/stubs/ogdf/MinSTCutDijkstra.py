# file stubs/ogdf/MinSTCutDijkstra.py generated from classogdf_1_1_min_s_t_cut_dijkstra
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
TCost = TypeVar('TCost')

class MinSTCutDijkstra(ogdf.MinSTCutModule[ TCost ], Generic[TCost]):

	"""Min-st-cut algorithm, that calculates the cut by calculating the shortest path between the faces adjacent to an edge between s and t, via the algorithm by Dijkstra on the dual graph."""

	def __init__(self) -> None:
		...

	@overload
	def call(self, graph : Graph, weight : EdgeArray[ TCost ], s : node, t : node, edgeList : List[edge], e_st : edge = None) -> bool:
		"""The actual algorithm call."""
		...

	@overload
	def call(self, graph : Graph, s : node, t : node, edgeList : List[edge], e_st : edge = None) -> bool:
		"""The actual algorithm call."""
		...
