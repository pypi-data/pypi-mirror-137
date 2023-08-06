# file stubs/ogdf/ClusterArray.py generated from classogdf_1_1_cluster_array
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
T = TypeVar('T')

class ClusterArray(ogdf.Array[ T ], ogdf.ClusterArrayBase, Generic[T]):

	"""Dynamic arrays indexed with clusters."""

	# Access methods

	def valid(self) -> bool:
		"""Returns true iff the array is associated with a graph."""
		...

	def graphOf(self) -> ClusterGraph:
		"""Returns a pointer to the associated cluster graph."""
		...

	@overload
	def __getitem__(self, c : cluster) -> T:
		"""Returns a reference to the element with indexc."""
		...

	@overload
	def __getitem__(self, c : cluster) -> T:
		"""Returns a reference to the element with indexc."""
		...

	@overload
	def __call__(self, c : cluster) -> T:
		"""Returns a reference to the element with indexc."""
		...

	@overload
	def __call__(self, c : cluster) -> T:
		"""Returns a reference to the element with indexc."""
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
		"""Returns an iterator to the first entry in the cluster array."""
		...

	@overload
	def begin(self) -> const_iterator:
		"""Returns a const iterator to the first entry in the cluster array."""
		...

	def cbegin(self) -> const_iterator:
		"""Returns a const iterator to the first entry in the cluster array."""
		...

	@overload
	def end(self) -> iterator:
		"""Returns an iterator to one-past-last entry in the cluster array."""
		...

	@overload
	def end(self) -> const_iterator:
		"""Returns a const iterator to one-past-last entry in the cluster array."""
		...

	def cend(self) -> const_iterator:
		"""Returns a const iterator to one-past-last entry in the cluster array."""
		...

	# Initialization and assignment

	@overload
	def init(self) -> None:
		"""Reinitializes the array. Associates the array with no cluster graph."""
		...

	@overload
	def init(self, C : ClusterGraph) -> None:
		"""Reinitializes the array. Associates the array withC."""
		...

	@overload
	def init(self, C : ClusterGraph, x : T) -> None:
		"""Reinitializes the array. Associates the array withC."""
		...

	def fill(self, x : T) -> None:
		"""Sets all array elements tox."""
		...

	@overload
	def __assign__(self, a : ClusterArray[ T ]) -> ClusterArray[ T ]:
		"""Assignment operator."""
		...

	@overload
	def __assign__(self, a : ClusterArray[ T ]) -> ClusterArray[ T ]:
		"""Assignment operator (move semantics)."""
		...

	# Helper functions

	def findSuccKey(self, key : key_type) -> key_type:
		...

	def findPredKey(self, key : key_type) -> key_type:
		...

	#: The type for cluster array const iterators.
	const_iterator : Type = internal.GraphArrayConstIterator[ClusterArray[ T ] ]

	#: The type for cluster array iterators.
	iterator : Type = internal.GraphArrayIterator[ClusterArray[ T ] ]

	#: The type for array keys.
	key_type : Type = cluster

	#: The type for array entries.
	value_type : Type = T

	@overload
	def __init__(self) -> None:
		"""Constructs an empty cluster array associated with no graph."""
		...

	@overload
	def __init__(self, A : ClusterArray[ T ]) -> None:
		"""Constructs a cluster array containing the elements ofA(move semantics)."""
		...

	@overload
	def __init__(self, A : ClusterArray[ T ]) -> None:
		"""Constructs a cluster array that is a copy ofA."""
		...

	@overload
	def __init__(self, C : ClusterGraph) -> None:
		"""Constructs a cluster array associated withC."""
		...

	@overload
	def __init__(self, C : ClusterGraph, x : T) -> None:
		"""Constructs a cluster array associated withC."""
		...

	@overload
	def __init__(self, C : ClusterGraph, x : T, size : int) -> None:
		"""Constructs a cluster array associated withCand a given size (for static use)."""
		...
