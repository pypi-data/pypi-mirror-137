# file stubs/ogdf/AdjElement.py generated from classogdf_1_1_adj_element
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
class AdjElement(ogdf.internal.GraphElement):

	"""Class for adjacency list elements."""

	def clockwiseFacePred(self) -> adjEntry:
		"""Returns the clockwise predecessor in face. Use faceCycleSucc instead!"""
		...

	def clockwiseFaceSucc(self) -> adjEntry:
		"""Returns the clockwise successor in face. Use faceCycleSucc instead!"""
		...

	def counterClockwiseFacePred(self) -> adjEntry:
		"""Returns the counter-clockwise predecessor in face."""
		...

	def counterClockwiseFaceSucc(self) -> adjEntry:
		"""Returns the counter-clockwise successor in face."""
		...

	def cyclicPred(self) -> adjEntry:
		"""Returns the cyclic predecessor in the adjacency list."""
		...

	def cyclicSucc(self) -> adjEntry:
		"""Returns the cyclic successor in the adjacency list."""
		...

	def faceCyclePred(self) -> adjEntry:
		"""Returns the cyclic predecessor in face."""
		...

	def faceCycleSucc(self) -> adjEntry:
		"""Returns the cyclic successor in face."""
		...

	def index(self) -> int:
		"""Returns the index of this adjacency element."""
		...

	def isBetween(self, adjBefore : adjEntry, adjAfter : adjEntry) -> bool:
		"""Returns whether this adjacency entry lies betweenadjBeforeandadjAfterin clockwise rotation."""
		...

	def isSource(self) -> bool:
		"""Returnstrueiff this is the source adjacency entry of the corresponding edge."""
		...

	def __edge__(self) -> None:
		"""Conversion to edge."""
		...

	def __node__(self) -> None:
		"""Casts to the node whose adjacency list contains this element."""
		...

	def pred(self) -> adjEntry:
		"""Returns the predecessor in the adjacency list."""
		...

	def succ(self) -> adjEntry:
		"""Returns the successor in the adjacency list."""
		...

	def theEdge(self) -> edge:
		"""Returns the edge associated with this adjacency entry."""
		...

	def theNode(self) -> node:
		"""Returns the node whose adjacency list contains this element."""
		...

	def twin(self) -> adjEntry:
		"""Returns the corresponding adjacency element associated with the same edge."""
		...

	def twinNode(self) -> node:
		"""Returns the associated node of the corresponding adjacency entry (shorthand fortwin()->theNode())."""
		...

	def compare(self, x : AdjElement, y : AdjElement) -> int:
		"""Standard Comparer."""
		...
