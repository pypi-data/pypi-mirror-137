# file stubs/ogdf/PlanRepInc.py generated from classogdf_1_1_plan_rep_inc
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
class PlanRepInc(ogdf.PlanRepUML, ogdf.GraphObserver):

	"""This class is only an adaption ofPlanRepfor the special incremental drawing case."""

	def nodeDeleted(self, v : node) -> None:
		"""In the case that the underlying incremental structure changes, we update this copy."""
		...

	def nodeAdded(self, v : node) -> None:
		"""Called by watched graph when a node is added Has to be implemented by derived classes."""
		...

	def edgeDeleted(self, e : edge) -> None:
		"""Called by watched graph when an edge is deleted Has to be implemented by derived classes."""
		...

	def edgeAdded(self, e : edge) -> None:
		"""Called by watched graph when an edge is added Has to be implemented by derived classes."""
		...

	def reInit(self) -> None:
		"""Called by watched graph when it is reinitialized Has to be implemented by derived classes."""
		...

	def cleared(self) -> None:
		"""Called by watched graph when its clear function is called Has to be implemented by derived classes."""
		...

	@overload
	def deleteTreeConnection(self, i : int, j : int) -> None:
		"""Deletes an edge again."""
		...

	@overload
	def deleteTreeConnection(self, i : int, j : int, E : CombinatorialEmbedding) -> None:
		...

	# Extension of methods defined by GraphCopy/PlanRep

	def split(self, e : edge) -> edge:
		"""Splits edge e, can be removed when edge status in edgetype m_treedge can be removed afterwards."""
		...

	@overload
	def __init__(self, UG : UMLGraph) -> None:
		"""Constructor for interactive updates (parts added step by step)"""
		...

	@overload
	def __init__(self, UG : UMLGraph, fixed : NodeArray[ bool ]) -> None:
		"""Constructor for incremental updates (whole graph already given). The part to stay fixed has fixed value set to true."""
		...

	def activateEdge(self, e : edge) -> None:
		"""Sets activity status to true and updates the structures."""
		...

	def activateNode(self, v : node) -> None:
		"""Sets activity status to true and updates the structures. Node activation activates all adjacent edges."""
		...

	def componentNumber(self, v : node) -> int:
		"""Component number."""
		...

	def getExtAdj(self, GC : GraphCopy, E : CombinatorialEmbedding) -> adjEntry:
		...

	def getExtAdjs(self, extAdjs : List[adjEntry]) -> None:
		"""Sets a list of adjentries on "external" faces of unconnected active parts of the current CC."""
		...

	def initActiveCC(self, i : int) -> None:
		"""Inits a CC only with active elements."""
		...

	def initMinActiveCC(self, i : int) -> node:
		"""Inits a CC with at least one active node, makes a node active if necessary and returns it. Returns nullptr otherwise."""
		...

	def makeTreeConnected(self, adjExternal : adjEntry) -> bool:
		"""Handles copies of original CCs that are split into unconnected parts of active nodes by connecting them tree-like, adding necessary edges at "external" nodes of the partial CCs. Note that this only makes sense when the CC parts are already correctly embedded."""
		...

	@overload
	def treeEdge(self, e : edge) -> bool:
		...

	@overload
	def treeEdge(self, i : int, j : int) -> edge:
		...

	def treeInit(self) -> bool:
		...

	def initActiveCCGen(self, i : int, minNode : bool) -> node:
		"""Initializes CC with active nodes (minNode ? at least one node)"""
		...

	def initMembers(self, UG : UMLGraph) -> None:
		...
