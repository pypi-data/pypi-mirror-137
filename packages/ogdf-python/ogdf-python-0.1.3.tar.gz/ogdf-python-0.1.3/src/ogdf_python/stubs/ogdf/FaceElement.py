# file stubs/ogdf/FaceElement.py generated from classogdf_1_1_face_element
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
class FaceElement(ogdf.internal.GraphElement):

	"""Faces in a combinatorial embedding."""

	#: Container maintaining the adjacency entries in the face.
	entries : internal.FaceAdjContainer = ...

	def firstAdj(self) -> adjEntry:
		"""Returns the first adjacency element in the face."""
		...

	def index(self) -> int:
		"""Returns the index of the face."""
		...

	def nextFaceEdge(self, adj : adjEntry) -> adjEntry:
		"""Returns the successor ofadjin the list of all adjacency elements in the face."""
		...

	def pred(self) -> face:
		"""Returns the predecessor in the list of all faces."""
		...

	def size(self) -> int:
		"""Returns the size of the face, i.e., the number of edges in the face."""
		...

	def succ(self) -> face:
		"""Returns the successor in the list of all faces."""
		...

	def compare(self, x : FaceElement, y : FaceElement) -> int:
		"""Standard Comparer."""
		...
