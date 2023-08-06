# file stubs/ogdf/EdgeArray.py generated from classogdf_1_1_edge_array
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
T = TypeVar('T')

class EdgeArray(ogdf.Array[ T ], ogdf.EdgeArrayBase, Generic[T]):

	"""Dynamic arrays indexed with edges."""

	# Access methods

	def valid(self) -> bool:
		"""Returns true iff the array is associated with a graph."""
		...

	def graphOf(self) -> Graph:
		"""Returns a pointer to the associated graph."""
		...

	@overload
	def __getitem__(self, e : edge) -> T:
		"""Returns a reference to the element with indexe."""
		...

	@overload
	def __getitem__(self, e : edge) -> T:
		"""Returns a reference to the element with indexe."""
		...

	@overload
	def __call__(self, e : edge) -> T:
		"""Returns a reference to the element with indexe."""
		...

	@overload
	def __call__(self, e : edge) -> T:
		"""Returns a reference to the element with indexe."""
		...

	@overload
	def __getitem__(self, adj : adjEntry) -> T:
		"""Returns a reference to the element with index edge ofadj."""
		...

	@overload
	def __getitem__(self, adj : adjEntry) -> T:
		"""Returns a reference to the element with index edge ofadj."""
		...

	@overload
	def __call__(self, adj : adjEntry) -> T:
		"""Returns a reference to the element with index edge ofadj."""
		...

	@overload
	def __call__(self, adj : adjEntry) -> T:
		"""Returns a reference to the element with index edge ofadj."""
		...

	@overload
	def __getitem__(self, index : int) -> T:
		"""Returns a reference to the element with indexindex."""
		...

	@overload
	def __getitem__(self, index : int) -> T:
		"""Returns a reference to the element with indexindex."""
		...

	# Iterators

	@overload
	def begin(self) -> iterator:
		"""Returns an iterator to the first entry in the edge array."""
		...

	@overload
	def begin(self) -> const_iterator:
		"""Returns a const iterator to the first entry in the edge array."""
		...

	def cbegin(self) -> const_iterator:
		"""Returns a const iterator to the first entry in the edge array."""
		...

	@overload
	def end(self) -> iterator:
		"""Returns an iterator to one-past-last entry in the edge array."""
		...

	@overload
	def end(self) -> const_iterator:
		"""Returns a const iterator to one-past-last entry in the edge array."""
		...

	def cend(self) -> const_iterator:
		"""Returns a const iterator to one-past-last entry in the edge array."""
		...

	# Initialization and assignment

	@overload
	def init(self) -> None:
		"""Reinitializes the array. Associates the array with no graph."""
		...

	@overload
	def init(self, G : Graph) -> None:
		"""Reinitializes the array. Associates the array withG."""
		...

	@overload
	def init(self, G : Graph, x : T) -> None:
		"""Reinitializes the array. Associates the array withG."""
		...

	def fill(self, x : T) -> None:
		"""Sets all array elements tox."""
		...

	@overload
	def __assign__(self, a : EdgeArray[ T ]) -> EdgeArray[ T ]:
		"""Assignment operator."""
		...

	@overload
	def __assign__(self, a : EdgeArray[ T ]) -> EdgeArray[ T ]:
		"""Assignment operator (move semantics)."""
		...

	# Helper functions

	def findSuccKey(self, key : key_type) -> key_type:
		...

	def findPredKey(self, key : key_type) -> key_type:
		...

	#: The type for edge array const iterators.
	const_iterator : Type = internal.GraphArrayConstIterator[EdgeArray[ T ] ]

	#: The type for edge array iterators.
	iterator : Type = internal.GraphArrayIterator[EdgeArray[ T ] ]

	#: The type for array keys.
	key_type : Type = edge

	#: The type for array entries.
	value_type : Type = T

	@overload
	def __init__(self) -> None:
		"""Constructs an empty edge array associated with no graph."""
		...

	@overload
	def __init__(self, A : EdgeArray[ T ]) -> None:
		"""Constructs an edge array that is a copy ofA."""
		...

	@overload
	def __init__(self, G : Graph) -> None:
		"""Constructs an edge array associated withG."""
		...

	@overload
	def __init__(self, G : Graph, x : T) -> None:
		"""Constructs an edge array associated withG."""
		...

	@overload
	def __init__(self, A : EdgeArray[ T ]) -> None:
		"""Constructs an edge array containing the elements ofA(move semantics)."""
		...
