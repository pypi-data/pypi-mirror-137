# file stubs/ogdf/steiner_tree/FullComponentWithExtraStore.py generated from classogdf_1_1steiner__tree_1_1_full_component_with_extra_store
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
T = TypeVar('T')

ExtraDataType = TypeVar('ExtraDataType')

class FullComponentWithExtraStore(ogdf.steiner_tree.FullComponentStore[ T, ExtraDataType ], Generic[T, ExtraDataType]):

	"""A data structure to store full components with extra data for each component."""

	@overload
	def extra(self, i : int) -> ExtraDataType:
		"""Returns a reference to the extra data of this full component."""
		...

	@overload
	def extra(self, i : int) -> ExtraDataType:
		"""Returns a const reference to the extra data of this full component."""
		...
