# file stubs/ogdf/HyperedgeArray.py generated from classogdf_1_1_hyperedge_array
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
T = TypeVar('T')

class HyperedgeArray(Generic[T]):

	"""Dynamic arrays indexed with nodes."""

	@overload
	def __init__(self) -> None:
		"""Constructs an empty hypernode array associated with no graph."""
		...

	@overload
	def __init__(self, H : Hypergraph, x : T) -> None:
		"""Constructs a hypernode array associated withH."""
		...

	def __destruct__(self) -> None:
		"""Destructor."""
		...

	@overload
	def init(self, H : Hypergraph) -> None:
		"""Reinitializes the array. Associates the array withH."""
		...

	@overload
	def init(self, H : Hypergraph, x : T) -> None:
		"""Reinitializes the array. Associates the array withH."""
		...

	def __assign__(self, a : HyperedgeArray[ T ]) -> HyperedgeArray[ T ]:
		"""Assignment operator."""
		...

	@overload
	def __getitem__(self, e : hyperedge) -> T:
		"""Returns a reference to the element with the index ofe."""
		...

	@overload
	def __getitem__(self, index : int) -> T:
		"""Returns a reference to the element with indexindex."""
		...

	@overload
	def __getitem__(self, index : int) -> T:
		"""Returns a reference to the element with indexindex."""
		...

	def reregister(self, H : Hypergraph) -> None:
		...

	def valid(self) -> bool:
		"""Returns true iff the array is associated with a hypergraph."""
		...
