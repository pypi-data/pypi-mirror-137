# file stubs/ogdf/energybased/fmmm/Edge.py generated from classogdf_1_1energybased_1_1fmmm_1_1_edge
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
class Edge(object):

	"""helping data structure for deleting parallel edges in classFMMMLayoutandMultilevel(needed for the bucket sort algorithm)"""

	def __init__(self) -> None:
		"""constructor"""
		...

	def get_angle(self) -> float:
		...

	def get_cut_vertex(self) -> node:
		...

	def get_edge(self) -> edge:
		...

	def get_Graph_ptr(self) -> Graph:
		...

	@overload
	def set_Edge(self, f : edge, i : float, c : node) -> None:
		...

	@overload
	def set_Edge(self, f : edge, g_ptr : Graph) -> None:
		...
