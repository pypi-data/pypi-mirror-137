# file stubs/ogdf/internal/FaceAdjIterator.py generated from classogdf_1_1internal_1_1_face_adj_iterator
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
class FaceAdjIterator(object):

	"""Forward iterator for adjacency entries in a face."""

	@overload
	def __init__(self) -> None:
		...

	@overload
	def __init__(self, adj : adjEntry) -> None:
		...

	@overload
	def __init__(self, adjFirst : adjEntry, adj : adjEntry) -> None:
		...

	@overload
	def __init__(self, _ : FaceAdjIterator) -> None:
		...

	def __ne__(self, other : FaceAdjIterator) -> bool:
		...

	def __deref__(self) -> adjEntry:
		...

	def __preinc__(self) -> FaceAdjIterator:
		...

	def __assign__(self, _ : FaceAdjIterator) -> FaceAdjIterator:
		...

	def __eq__(self, other : FaceAdjIterator) -> bool:
		...
