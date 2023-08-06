# file stubs/ogdf/ExpansionGraph.py generated from classogdf_1_1_expansion_graph
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
class ExpansionGraph(ogdf.Graph):

	"""Represents expansion graph of each biconnected component of a given digraph, i.e., each vertex v with in- and outdegree greater than 1 is expanded into two vertices x and y connected by an edge x->y such that all incoming edges are moved from v to x and all outgoing edges from v to y."""

	def __init__(self, G : Graph) -> None:
		...

	def adjacentComponents(self, v : node) -> SList[  int ]:
		...

	def component(self, i : int) -> SListPure[edge]:
		...

	def componentNumber(self, e : edge) -> int:
		...

	def copy(self, vG : node) -> node:
		...

	@overload
	def init(self, G : Graph) -> None:
		...

	@overload
	def init(self, i : int) -> None:
		...

	def numberOfBCs(self) -> int:
		...

	@overload
	def original(self, e : edge) -> edge:
		...

	@overload
	def original(self, v : node) -> node:
		...

	def representative(self, v : node) -> node:
		...

	def setComponentNumber(self, e : edge, i : int) -> None:
		...

	def setOriginal(self, vCopy : node, vOriginal : node) -> None:
		...
