# file stubs/ogdf/EdgeComparerSimple.py generated from classogdf_1_1_edge_comparer_simple
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
class EdgeComparerSimple(ogdf.VComparer[ adjEntry ]):

	"""Compares incident edges of a node based on the position of the last bend point or the position of the adjacent node given by the layout information of the graph."""

	def __init__(self, AG : GraphAttributes, v : node, useBends : bool = True) -> None:
		...

	def compare(self, x : adjEntry, y : adjEntry) -> int:
		"""Comparesxandyand returns the result as an integer."""
		...
