# file stubs/ogdf/PlanRepExpansion/__init__.py generated from classogdf_1_1_plan_rep_expansion
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
class PlanRepExpansion(ogdf.Graph):

	"""Planarized representations (of a connected component) of a graph."""

	# Acess methods

	@overload
	def original(self) -> Graph:
		"""Returns a reference to the original graph."""
		...

	@overload
	def original(self, v : node) -> node:
		"""Returns the original node ofv, or 0 ifvis a dummy."""
		...

	def expansion(self, vOrig : node) -> List[node]:
		"""Returns the list of copy nodes ofvOrig."""
		...

	@overload
	def copy(self, vOrig : node) -> node:
		"""Returns the first copy node ofvOrig."""
		...

	def originalEdge(self, e : edge) -> edge:
		"""Returns the original edge ofe, or 0 ifehas none (e.g.,ebelongs to a node split)."""
		...

	def chain(self, eOrig : edge) -> List[edge]:
		"""Returns the insertion path of edgeeOrig."""
		...

	@overload
	def copy(self, eOrig : edge) -> edge:
		"""Returns the first edge ineOrig'sinsertion path."""
		...

	def splittable(self, v : node) -> bool:
		"""Returns true iffvis splittable."""
		...

	def splittableOrig(self, vOrig : node) -> bool:
		"""Returns true iffvOrigis splittable."""
		...

	def nodeSplitOf(self, e : edge) -> NodeSplit:
		"""Returns the node split associated withe, or 0 if none (e.g.,ebelongs to an original edge)."""
		...

	def numberOfNodeSplits(self) -> int:
		"""Returns the number of node splits."""
		...

	def numberOfSplittedNodes(self) -> int:
		...

	def nodeSplits(self) -> List[NodeSplit]:
		"""Returns the list of node splits."""
		...

	def setOrigs(self, e : edge, eOrig : edge, ns : nodeSplit) -> List[edge]:
		"""Sets the original edge and corresponding node split ofeand returns the corresponding insertion path."""
		...

	def position(self, e : edge) -> ListConstIterator[edge]:
		...

	def isPseudoCrossing(self, v : node) -> bool:
		...

	def computeNumberOfCrossings(self) -> int:
		"""Computes the number of crossings."""
		...

	# Processing connected components

	def numberOfCCs(self) -> int:
		"""Returns the number of connected components in the original graph."""
		...

	def currentCC(self) -> int:
		"""Returns the index of the current connected component (-1 if not yet initialized)."""
		...

	@overload
	def nodesInCC(self, i : int) -> List[node]:
		"""Returns the list of (original) nodes in connected componenti."""
		...

	@overload
	def nodesInCC(self) -> List[node]:
		"""Returns the list of (original) nodes in the current connected component."""
		...

	def initCC(self, i : int) -> None:
		"""Initializes the planarized representation for connected componenti."""
		...

	# Update operations

	def split(self, e : edge) -> edge:
		"""Splits edgeeinto two edges introducing a new node."""
		...

	def unsplit(self, eIn : edge, eOut : edge) -> None:
		"""Undoes a split operation."""
		...

	def delEdge(self, e : edge) -> None:
		"""Removes edgeefrom the planarized expansion."""
		...

	def embed(self) -> bool:
		"""Embeds the planarized expansion; returns true iff it is planar."""
		...

	def insertEdgePath(self, eOrig : edge, ns : nodeSplit, vStart : node, vEnd : node, eip : List[Crossing], eSrc : edge, eTgt : edge) -> None:
		...

	def insertEdgePathEmbedded(self, eOrig : edge, ns : nodeSplit, E : CombinatorialEmbedding, crossedEdges : List[Tuple2[adjEntry,adjEntry] ]) -> None:
		"""Inserts an edge or a node split according to insertion pathcrossedEdges."""
		...

	def removeEdgePathEmbedded(self, E : CombinatorialEmbedding, eOrig : edge, ns : nodeSplit, newFaces : FaceSet[ False ], mergedNodes : NodeSet[ False ], oldSrc : node, oldTgt : node) -> None:
		"""Removes the insertion path ofeOrigorns."""
		...

	def removeEdgePath(self, eOrig : edge, ns : nodeSplit, oldSrc : node, oldTgt : node) -> None:
		"""Removes the insertion path ofeOrigorns."""
		...

	@overload
	def contractSplit(self, ns : nodeSplit, E : CombinatorialEmbedding) -> None:
		"""Removes an (unneccessary) node split consisting of a single edge."""
		...

	@overload
	def contractSplit(self, ns : nodeSplit) -> None:
		"""Removes an (unneccessary) node split consisting of a single edge."""
		...

	@overload
	def unsplitExpandNode(self, u : node, eContract : edge, eExpand : edge, E : CombinatorialEmbedding) -> edge:
		"""Unsplits a superfluous expansion node of degree 2."""
		...

	@overload
	def unsplitExpandNode(self, u : node, eContract : edge, eExpand : edge) -> edge:
		"""Unsplits a superfluous expansion node of degree 2."""
		...

	@overload
	def enlargeSplit(self, v : node, e : edge, E : CombinatorialEmbedding) -> edge:
		"""Splits edgeeand introduces a new node split starting atv."""
		...

	@overload
	def enlargeSplit(self, v : node, e : edge) -> edge:
		"""Splits edgeeand introduces a new node split starting atv."""
		...

	@overload
	def splitNodeSplit(self, e : edge, E : CombinatorialEmbedding) -> edge:
		"""Introduces a new node split by splitting an exisiting node split."""
		...

	@overload
	def splitNodeSplit(self, e : edge) -> edge:
		"""Introduces a new node split by splitting an exisiting node split."""
		...

	@overload
	def removeSelfLoop(self, e : edge, E : CombinatorialEmbedding) -> None:
		"""Removes a self-loope= (u,u)."""
		...

	@overload
	def removeSelfLoop(self, e : edge) -> None:
		...

	def convertDummy(self, u : node, vOrig : node, ns : PlanRepExpansion.nodeSplit) -> PlanRepExpansion.nodeSplit:
		"""Converts a dummy nodeuto a copy of an original nodevOrig."""
		...

	def separateDummy(self, adj_1 : adjEntry, adj_2 : adjEntry, vStraight : node, isSrc : bool) -> edge:
		...

	def resolvePseudoCrossing(self, v : node) -> None:
		...

	# Miscelleaneous

	#: Pointer to a node split.
	nodeSplit : Type = PlanRepExpansion.NodeSplit

	@overload
	def __init__(self, G : Graph) -> None:
		"""Creates a planarized expansion of graphG."""
		...

	@overload
	def __init__(self, G : Graph, splittableNodes : List[node]) -> None:
		"""Creates a planarized expansion of graphGwith given splittable nodes."""
		...

	def __destruct__(self) -> None:
		...
