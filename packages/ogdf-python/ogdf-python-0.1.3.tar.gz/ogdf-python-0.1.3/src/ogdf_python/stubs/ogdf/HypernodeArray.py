# file stubs/ogdf/HypernodeArray.py generated from classogdf_1_1_hypernode_array
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
T = TypeVar('T')

class HypernodeArray(Generic[T]):

	"""Dynamic arrays indexed with hypernodes."""

	@overload
	def __init__(self) -> None:
		"""Constructs an empty hypernode array associated with no hypergraph."""
		...

	@overload
	def __init__(self, H : Hypergraph, x : T) -> None:
		"""Constructs a hypernode array associated withH."""
		...

	def __destruct__(self) -> None:
		...

	@overload
	def init(self, H : Hypergraph) -> None:
		"""Reinitializes the array. Associates the array withH."""
		...

	@overload
	def init(self, H : Hypergraph, x : T) -> None:
		"""Reinitializes the array. Associates the array withH."""
		...

	def __assign__(self, a : HypernodeArray[ T ]) -> HypernodeArray[ T ]:
		"""Assignment operator."""
		...

	@overload
	def __getitem__(self, v : hypernode) -> T:
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

	def reregister(self, H : Hypergraph) -> None:
		...
