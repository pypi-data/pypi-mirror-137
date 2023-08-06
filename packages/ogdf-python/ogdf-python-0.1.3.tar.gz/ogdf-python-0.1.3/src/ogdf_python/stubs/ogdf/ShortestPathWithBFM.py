# file stubs/ogdf/ShortestPathWithBFM.py generated from classogdf_1_1_shortest_path_with_b_f_m
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
class ShortestPathWithBFM(ogdf.ShortestPathModule):

	"""Computes single-source shortest-paths with Bellman-Ford-Moore's algorithm."""

	def __init__(self) -> None:
		...

	def call(self, G : Graph, s : node, length : EdgeArray[  int ], d : NodeArray[  int ], pi : NodeArray[edge]) -> bool:
		...
