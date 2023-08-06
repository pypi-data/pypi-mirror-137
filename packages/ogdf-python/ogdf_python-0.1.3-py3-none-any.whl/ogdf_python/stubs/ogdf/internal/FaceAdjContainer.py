# file stubs/ogdf/internal/FaceAdjContainer.py generated from classogdf_1_1internal_1_1_face_adj_container
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
class FaceAdjContainer(object):

	"""Container for the adjacency entries in a face."""

	iterator : Type = FaceAdjIterator

	def begin(self) -> iterator:
		...

	def end(self) -> iterator:
		...
