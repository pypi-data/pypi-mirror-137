# file stubs/ogdf/FaceSet.py generated from classogdf_1_1_face_set
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
OtherSupportsFastSizeQuery = TypeVar('OtherSupportsFastSizeQuery')

SupportFastSizeQuery = TypeVar('SupportFastSizeQuery')

class FaceSet(Generic[SupportFastSizeQuery]):

	"""Face sets."""

	ListType : Type = Union[List[face], ListPure[face]]

	@overload
	def __init__(self, E : CombinatorialEmbedding) -> None:
		"""Creates an empty face set associated with combinatorial embeddingE."""
		...

	@overload
	def __init__(self, other : FaceSet[ OtherSupportsFastSizeQuery ]) -> None:
		"""Copy constructor."""
		...

	def clear(self) -> None:
		"""Removes all faces from this set-."""
		...

	def embeddingOf(self) -> ConstCombinatorialEmbedding:
		"""Returns the associated combinatorial embedding."""
		...

	def faces(self) -> ListType:
		"""Returns a reference to the list of faces contained in this set."""
		...

	def insert(self, f : face) -> None:
		"""Inserts facefinto this set."""
		...

	def isMember(self, f : face) -> bool:
		"""Returnstrueiff facefis contained in this set."""
		...

	def __assign__(self, other : FaceSet[ OtherSupportsFastSizeQuery ]) -> FaceSet:
		"""Assignment operator."""
		...

	def remove(self, f : face) -> None:
		"""Removes faceffrom this set."""
		...

	def size(self) -> int:
		"""Returns the number of faces in this set."""
		...
