# file stubs/ogdf/NodeArray.py generated from classogdf_1_1_node_array
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
T = TypeVar('T')

class NodeArray(Generic[T]):

	"""Dynamic arrays indexed with nodes."""

	# Access methods

	def valid(self) -> bool:
		"""Returns true iff the array is associated with a graph."""
		...

	def graphOf(self) -> Graph:
		"""Returns a pointer to the associated graph."""
		...

	@overload
	def __getitem__(self, v : node) -> T:
		"""Returns a reference to the element with indexv."""
		...

	@overload
	def __getitem__(self, v : node) -> T:
		"""Returns a reference to the element with indexv."""
		...

	@overload
	def __call__(self, v : node) -> T:
		"""Returns a reference to the element with indexv."""
		...

	@overload
	def __call__(self, v : node) -> T:
		"""Returns a reference to the element with indexv."""
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
		"""Returns an iterator to the first entry in the node array."""
		...

	@overload
	def begin(self) -> const_iterator:
		"""Returns a const iterator to the first entry in the node array."""
		...

	def cbegin(self) -> const_iterator:
		"""Returns a const iterator to the first entry in the node array."""
		...

	@overload
	def end(self) -> iterator:
		"""Returns an iterator to one-past-last entry in the node array."""
		...

	@overload
	def end(self) -> const_iterator:
		"""Returns a const iterator to one-past-last entry in the node array."""
		...

	def cend(self) -> const_iterator:
		"""Returns a const iterator to one-past-last entry in the node array."""
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
	def __assign__(self, a : NodeArray[ T ]) -> NodeArray[ T ]:
		"""Assignment operator."""
		...

	@overload
	def __assign__(self, a : NodeArray[ T ]) -> NodeArray[ T ]:
		"""Assignment operator (move semantics)."""
		...

	# Helper functions

	def findSuccKey(self, key : key_type) -> key_type:
		...

	def findPredKey(self, key : key_type) -> key_type:
		...

	#: The type for node array const iterators.
	const_iterator : Type = internal.GraphArrayConstIterator[NodeArray[ T ] ]

	#: The type for node array iterators.
	iterator : Type = internal.GraphArrayIterator[NodeArray[ T ] ]

	#: The type for array keys.
	key_type : Type = node

	#: The type for array entries.
	value_type : Type = T

	@overload
	def __init__(self) -> None:
		"""Constructs an empty node array associated with no graph."""
		...

	@overload
	def __init__(self, G : Graph) -> None:
		"""Constructs a node array associated withG."""
		...

	@overload
	def __init__(self, G : Graph, x : T) -> None:
		"""Constructs a node array associated withG."""
		...

	@overload
	def __init__(self, A : NodeArray[ T ]) -> None:
		"""Constructs a node array that is a copy ofA."""
		...

	@overload
	def __init__(self, A : NodeArray[ T ]) -> None:
		"""Constructs a node array containing the elements ofA(move semantics)."""
		...
