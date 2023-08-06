# file stubs/ogdf/Graph/CCsInfo.py generated from classogdf_1_1_graph_1_1_c_cs_info
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
class CCsInfo(object):

	"""Info structure for maintaining connected components."""

	@overload
	def __init__(self) -> None:
		"""Creates a info structure associated with no graph."""
		...

	@overload
	def __init__(self, G : Graph) -> None:
		"""Creates a info structure associated with graphG."""
		...

	def constGraph(self) -> Graph:
		"""Returns the associated graph."""
		...

	def e(self, i : int) -> edge:
		"""Returns the edge with indexi."""
		...

	def numberOfCCs(self) -> int:
		"""Returns the number of connected components."""
		...

	def numberOfEdges(self, cc : int) -> int:
		"""Returns the number of edges in connected componentcc."""
		...

	def numberOfNodes(self, cc : int) -> int:
		"""Returns the number of nodes in connected componentcc."""
		...

	def startEdge(self, cc : int) -> int:
		"""Returns the index of the first edge in connected componentcc."""
		...

	def startNode(self, cc : int) -> int:
		"""Returns the index of the first node in connected componentcc."""
		...

	def stopEdge(self, cc : int) -> int:
		"""Returns the index of (one past) the last edge in connected componentcc."""
		...

	def stopNode(self, cc : int) -> int:
		"""Returns the index of (one past) the last node in connected componentcc."""
		...

	def v(self, i : int) -> node:
		"""Returns the node with indexi."""
		...
