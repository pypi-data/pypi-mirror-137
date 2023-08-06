# file stubs/ogdf/cluster_planarity/EdgeVar.py generated from classogdf_1_1cluster__planarity_1_1_edge_var
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
class EdgeVar(abacus.Variable):

	class EdgeType(enum.Enum):

		Original = enum.auto()

		Connect = enum.auto()

	@overload
	def __init__(self, master : abacus.Master, obj : float, lbound : float, source : node, target : node) -> None:
		"""Simple version for cplanarity testing (only connect edges allowed, lower bound given)"""
		...

	@overload
	def __init__(self, master : abacus.Master, obj : float, eType : EdgeType, source : node, target : node) -> None:
		...

	@overload
	def __init__(self, master : abacus.Master, obj : float, source : node, target : node) -> None:
		"""Simple version for cplanarity testing (only connect edges allowed)"""
		...

	def __destruct__(self) -> None:
		...

	def printMe(self, out : std.ostream) -> None:
		...

	def sourceNode(self) -> node:
		...

	def targetNode(self) -> node:
		...

	def theEdge(self) -> edge:
		...

	def theEdgeType(self) -> EdgeType:
		...
