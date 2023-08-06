# file stubs/ogdf/FaceArrayBase.py generated from classogdf_1_1_face_array_base
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
class FaceArrayBase(object):

	"""Abstract base class for face arrays."""

	#: The associated combinatorial embedding.
	m_pEmbedding : ConstCombinatorialEmbedding = ...

	@overload
	def __init__(self) -> None:
		"""Initializes a face array not associated with a combinatorial embedding."""
		...

	@overload
	def __init__(self, pE : ConstCombinatorialEmbedding) -> None:
		"""Initializes a face array associated withpE."""
		...

	@overload
	def __init__(self, base : FaceArrayBase) -> None:
		"""Moves face arraybaseto this face array."""
		...

	def __destruct__(self) -> None:
		...

	def enlargeTable(self, newTableSize : int) -> None:
		"""Virtual function called when table size has to be enlarged."""
		...

	def moveRegister(self, base : FaceArrayBase) -> None:
		"""Moves array registration frombaseto this array."""
		...

	def reinit(self, initTableSize : int) -> None:
		"""Virtual function called when table has to be reinitialized."""
		...

	def reregister(self, pE : ConstCombinatorialEmbedding) -> None:
		"""Associates the array with a new combinatorial embedding."""
		...
