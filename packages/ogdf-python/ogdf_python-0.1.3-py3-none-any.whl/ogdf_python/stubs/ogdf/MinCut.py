# file stubs/ogdf/MinCut.py generated from classogdf_1_1_min_cut
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
class MinCut(object):

	"""Computes a minimum cut in a graph."""

	def __init__(self, G : Graph, w : EdgeArray[ float ]) -> None:
		...

	def __destruct__(self) -> None:
		...

	def cutEdges(self, edges : List[edge], G : Graph) -> None:
		...

	def minCutValue(self) -> float:
		...

	def minimumCut(self) -> float:
		...

	def partition(self, nodes : List[node]) -> None:
		...
