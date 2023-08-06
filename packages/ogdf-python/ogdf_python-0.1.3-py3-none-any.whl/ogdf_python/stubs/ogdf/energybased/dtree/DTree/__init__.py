# file stubs/ogdf/energybased/dtree/DTree/__init__.py generated from classogdf_1_1energybased_1_1dtree_1_1_d_tree
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
IntType = TypeVar('IntType')

Dim = TypeVar('Dim')

class DTree(Generic[IntType, Dim]):

	"""Implentation of the reduced quadtree for Dim dimensions."""

	#: the maximum number of children per node = 2^d
	MaxNumChildrenPerNode : int = ...

	def __init__(self, numPoints : int) -> None:
		"""constructor"""
		...

	def __destruct__(self) -> None:
		"""destructor"""
		...

	def adjustPointInfo(self, curr : int) -> None:
		"""used to update the first and numPoints of inner nodes by linkNodes"""
		...

	def build(self) -> None:
		"""Does all required steps except the allocate, deallocate, randomPoints."""
		...

	def child(self, i : int, j : int) -> int:
		"""returns the index of the j th child of node i"""
		...

	@overload
	def countPoints(self) -> int:
		"""Just for fun: traverse the tree and count the points in the leaves."""
		...

	@overload
	def countPoints(self, curr : int) -> int:
		"""Just for fun: traverse the tree and count the points in the leaves."""
		...

	@overload
	def linkNodes(self) -> None:
		"""The Recursive Bottom-Up Construction (recursion start)"""
		...

	@overload
	def linkNodes(self, curr : int, maxLevel : int) -> int:
		"""The Recursive Bottom-Up Construction."""
		...

	def maxNumNodes(self) -> int:
		"""returns the maximum number of nodes (and the max index of a node)"""
		...

	def mergeWithNext(self, curr : int) -> None:
		"""Merges curr with next node in the chain (used by linkNodes)"""
		...

	@overload
	def node(self, i : int) -> Node:
		"""Just to access the nodes a little bit easier."""
		...

	@overload
	def node(self, i : int) -> Node:
		"""Just to access the nodes a little bit easier."""
		...

	def numChilds(self, i : int) -> int:
		"""returns the number of children of node i"""
		...

	@overload
	def numPoints(self) -> int:
		"""returns the number of points the quadtree contains"""
		...

	@overload
	def numPoints(self, i : int) -> int:
		"""returns the number of points covered by this subtree"""
		...

	@overload
	def point(self, i : int) -> Point:
		"""returns the ith point in the input sequence"""
		...

	@overload
	def point(self, i : int, j : int) -> int:
		"""returns the index of the jth point covered by i's subtree."""
		...

	def prepareMortonOrder(self) -> None:
		"""Prepares the morton numbers for sorting."""
		...

	def prepareNodeLayer(self) -> None:
		"""Prepares both the leaf and inner node layer."""
		...

	def rootIndex(self) -> int:
		"""returns the index of the root node"""
		...

	def setPoint(self, i : int, d : int, value : IntType) -> None:
		"""sets the point to the given grid coords"""
		...

	def sortMortonNumbers(self) -> None:
		"""Sorts the points by morton number."""
		...
