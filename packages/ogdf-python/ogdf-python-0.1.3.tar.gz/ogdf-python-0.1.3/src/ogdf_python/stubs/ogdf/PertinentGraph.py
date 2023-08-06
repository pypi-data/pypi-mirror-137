# file stubs/ogdf/PertinentGraph.py generated from classogdf_1_1_pertinent_graph
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
class PertinentGraph(object):

	"""Pertinent graphs of nodes in an SPQR-tree."""

	#: corresp.
	m_origE : EdgeArray[edge] = ...

	#: corresp.
	m_origV : NodeArray[node] = ...

	#: actual graph
	m_P : Graph = ...

	#: reference edge (in skeleton(m_vT))
	m_skRefEdge : edge = ...

	#: reference edge (inm_P)
	m_vEdge : edge = ...

	#: corresponding tree node
	m_vT : node = ...

	def __init__(self) -> None:
		"""Creates an empty instance of typePertinentGraph."""
		...

	@overload
	def getGraph(self) -> Graph:
		"""Returns a reference toG(vT)."""
		...

	@overload
	def getGraph(self) -> Graph:
		"""Returns a reference toG(vT)."""
		...

	def init(self, vT : node) -> None:
		"""Initializationof a pertinent graph of tree nodevT."""
		...

	@overload
	def original(self, e : edge) -> edge:
		"""Returns the edge inGthat corresponds toe."""
		...

	@overload
	def original(self, v : node) -> node:
		"""Returns the vertex inGthat corresponds tov."""
		...

	def referenceEdge(self) -> edge:
		"""Returns the edge inG(vT) corresponding to the reference edge in skeleton ofvT."""
		...

	def skeletonReferenceEdge(self) -> edge:
		"""Returns the reference edge in skeleton ofvT."""
		...

	def treeNode(self) -> node:
		"""Returns the tree nodevTinTwhose pertinent graph is this one."""
		...
