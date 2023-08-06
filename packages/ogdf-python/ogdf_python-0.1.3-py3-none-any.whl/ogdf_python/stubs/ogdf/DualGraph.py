# file stubs/ogdf/DualGraph.py generated from classogdf_1_1_dual_graph
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
class DualGraph(ogdf.CombinatorialEmbedding):

	"""A dual graph including its combinatorial embedding of an embedded graph."""

	#: The corresponding edge in the dual graph.
	m_dualEdge : EdgeArray[edge] = ...

	#: The corresponding face in embedding of the dual graph.
	m_dualFace : NodeArray[face] = ...

	#: The corresponding node in the dual graph.
	m_dualNode : FaceArray[node] = ...

	#: The corresponding edge in the primal graph.
	m_primalEdge : EdgeArray[edge] = ...

	#: The embedding of the primal graph.
	m_primalEmbedding : ConstCombinatorialEmbedding = ...

	#: The corresponding facee in the embedding of the primal graph.
	m_primalFace : NodeArray[face] = ...

	#: The corresponding node in the primal graph.
	m_primalNode : FaceArray[node] = ...

	def __init__(self, CE : ConstCombinatorialEmbedding) -> None:
		"""Constructor; creates dual graph and its combinatorial embedding."""
		...

	def __destruct__(self) -> None:
		"""Destructor."""
		...

	def dualEdge(self, e : edge) -> edge:
		"""Returns the edge in the dual graph corresponding toe."""
		...

	def dualFace(self, v : node) -> face:
		"""Returns the face in the embedding of the dual graph corresponding tov."""
		...

	def dualNode(self, f : face) -> node:
		"""Returns the node in the dual graph corresponding tof."""
		...

	def getPrimalEmbedding(self) -> ConstCombinatorialEmbedding:
		"""Returns a reference to the combinatorial embedding of the primal graph."""
		...

	def getPrimalGraph(self) -> Graph:
		"""Returns a reference to the primal graph."""
		...

	def primalEdge(self, e : edge) -> edge:
		"""Returns the edge in the primal graph corresponding toe."""
		...

	def primalFace(self, v : node) -> face:
		"""Returns the face in the embedding of the primal graph corresponding tov."""
		...

	def primalNode(self, f : face) -> node:
		"""Returns the node in the primal graph corresponding tof."""
		...
