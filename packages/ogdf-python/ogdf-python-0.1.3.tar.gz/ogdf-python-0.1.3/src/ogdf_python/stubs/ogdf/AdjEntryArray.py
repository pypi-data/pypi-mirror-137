# file stubs/ogdf/AdjEntryArray.py generated from classogdf_1_1_adj_entry_array
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
T = TypeVar('T')

class AdjEntryArray(ogdf.Array[ T ], ogdf.AdjEntryArrayBase, Generic[T]):

	"""Dynamic arrays indexed with adjacency entries."""

	# Access methods

	def valid(self) -> bool:
		"""Returns true iff the array is associated with a graph."""
		...

	def graphOf(self) -> Graph:
		"""Returns a pointer to the associated graph."""
		...

	@overload
	def __getitem__(self, adj : adjEntry) -> T:
		"""Returns a reference to the element with indexadj."""
		...

	@overload
	def __getitem__(self, adj : adjEntry) -> T:
		"""Returns a reference to the element with indexadj."""
		...

	@overload
	def __call__(self, adj : adjEntry) -> T:
		"""Returns a reference to the element with indexadj."""
		...

	@overload
	def __call__(self, adj : adjEntry) -> T:
		"""Returns a reference to the element with indexadj."""
		...

	# Iterators

	@overload
	def begin(self) -> iterator:
		"""Returns an iterator to the first entry in the array."""
		...

	@overload
	def begin(self) -> const_iterator:
		"""Returns a const iterator to the first entry in the array."""
		...

	def cbegin(self) -> const_iterator:
		"""Returns a const iterator to the first entry in the array."""
		...

	@overload
	def end(self) -> iterator:
		"""Returns an iterator to one-past-last entry in the array."""
		...

	@overload
	def end(self) -> const_iterator:
		"""Returns a const iterator to one-past-last entry in the array."""
		...

	def cend(self) -> const_iterator:
		"""Returns a const iterator to one-past-last entry in the array."""
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
	def __assign__(self, A : AdjEntryArray[ T ]) -> AdjEntryArray[ T ]:
		"""Assignment operator."""
		...

	@overload
	def __assign__(self, a : AdjEntryArray[ T ]) -> AdjEntryArray[ T ]:
		"""Assignment operator (move semantics)."""
		...

	# Helper functions

	def findSuccKey(self, adj : adjEntry) -> adjEntry:
		"""Returns the key succeedingadj."""
		...

	def findPredKey(self, adj : adjEntry) -> adjEntry:
		"""Returns the key preceedingadj."""
		...

	#: The type for adjEntry array const iterators.
	const_iterator : Type = internal.GraphArrayConstIterator[AdjEntryArray[ T ] ]

	#: The type for adjEntry array iterators.
	iterator : Type = internal.GraphArrayIterator[AdjEntryArray[ T ] ]

	#: The type for array keys.
	key_type : Type = adjEntry

	#: The type for array entries.
	value_type : Type = T

	@overload
	def __init__(self) -> None:
		"""Constructs an empty adjacency entry array associated with no graph."""
		...

	@overload
	def __init__(self, A : AdjEntryArray[ T ]) -> None:
		"""Constructs an adjacency entry array containing the elements ofA(move semantics)."""
		...

	@overload
	def __init__(self, A : AdjEntryArray[ T ]) -> None:
		"""Constructs an adjacency entry array that is a copy ofA."""
		...

	@overload
	def __init__(self, G : Graph) -> None:
		"""Constructs an adjacency entry array associated withG."""
		...

	@overload
	def __init__(self, G : Graph, x : T) -> None:
		"""Constructs an adjacency entry array associated withG."""
		...
