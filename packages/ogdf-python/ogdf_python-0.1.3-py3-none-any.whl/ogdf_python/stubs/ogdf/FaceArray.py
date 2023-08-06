# file stubs/ogdf/FaceArray.py generated from classogdf_1_1_face_array
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
T = TypeVar('T')

class FaceArray(Generic[T]):

	"""Dynamic arrays indexed with faces of a combinatorial embedding."""

	# Access methods

	def valid(self) -> bool:
		"""Returns true iff the array is associated with a combinatorial embedding."""
		...

	def embeddingOf(self) -> ConstCombinatorialEmbedding:
		"""Returns a pointer to the associated combinatorial embedding."""
		...

	@overload
	def __getitem__(self, f : face) -> T:
		"""Returns a reference to the element with indexf."""
		...

	@overload
	def __getitem__(self, f : face) -> T:
		"""Returns a reference to the element with indexf."""
		...

	@overload
	def __call__(self, f : face) -> T:
		"""Returns a reference to the element with indexf."""
		...

	@overload
	def __call__(self, f : face) -> T:
		"""Returns a reference to the element with indexf."""
		...

	# Iterators

	@overload
	def begin(self) -> iterator:
		"""Returns an iterator to the first entry in the face array."""
		...

	@overload
	def begin(self) -> const_iterator:
		"""Returns a const iterator to the first entry in the face array."""
		...

	def cbegin(self) -> const_iterator:
		"""Returns a const iterator to the first entry in the face array."""
		...

	@overload
	def end(self) -> iterator:
		"""Returns an iterator to one-past-last entry in the face array."""
		...

	@overload
	def end(self) -> const_iterator:
		"""Returns a const iterator to one-past-last entry in the face array."""
		...

	def cend(self) -> const_iterator:
		"""Returns a const iterator to one-past-last entry in the face array."""
		...

	# Initialization and assignment

	@overload
	def init(self) -> None:
		"""Reinitializes the array. Associates the array with no combinatorial embedding."""
		...

	@overload
	def init(self, E : ConstCombinatorialEmbedding) -> None:
		"""Reinitializes the array. Associates the array withE."""
		...

	@overload
	def init(self, E : ConstCombinatorialEmbedding, x : T) -> None:
		"""Reinitializes the array. Associates the array withE."""
		...

	def fill(self, x : T) -> None:
		"""Sets all array elements tox."""
		...

	@overload
	def __assign__(self, a : FaceArray[ T ]) -> FaceArray[ T ]:
		"""Assignment operator."""
		...

	@overload
	def __assign__(self, a : FaceArray[ T ]) -> FaceArray[ T ]:
		"""Assignment operator (move semantics)."""
		...

	# Helper functions

	def findSuccKey(self, key : key_type) -> key_type:
		...

	def findPredKey(self, key : key_type) -> key_type:
		...

	#: The type for face array const iterators.
	const_iterator : Type = internal.GraphArrayConstIterator[FaceArray[ T ] ]

	#: The type for face array iterators.
	iterator : Type = internal.GraphArrayIterator[FaceArray[ T ] ]

	#: The type for array keys.
	key_type : Type = face

	#: The type for array entries.
	value_type : Type = T

	@overload
	def __init__(self) -> None:
		"""Constructs an empty face array associated with no combinatorial embedding."""
		...

	@overload
	def __init__(self, E : ConstCombinatorialEmbedding) -> None:
		"""Constructs a face array associated withE."""
		...

	@overload
	def __init__(self, E : ConstCombinatorialEmbedding, x : T) -> None:
		"""Constructs a face array associated withE."""
		...

	@overload
	def __init__(self, A : FaceArray[ T ]) -> None:
		"""Constructs an face array that is a copy ofA."""
		...

	@overload
	def __init__(self, A : FaceArray[ T ]) -> None:
		"""Constructs a face array containing the elements ofA(move semantics)."""
		...
