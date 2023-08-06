# file stubs/ogdf/MinSTCutBFS.py generated from classogdf_1_1_min_s_t_cut_b_f_s
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
TCost = TypeVar('TCost')

class MinSTCutBFS(ogdf.MinSTCutModule[ TCost ], Generic[TCost]):

	"""Min-st-cut algorithm, that calculates the cut by doing a depth first search over the dual graph of of an st-planar input graph."""

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
