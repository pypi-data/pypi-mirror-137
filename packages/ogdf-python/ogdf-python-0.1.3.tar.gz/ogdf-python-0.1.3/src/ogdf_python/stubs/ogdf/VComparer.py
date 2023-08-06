# file stubs/ogdf/VComparer.py generated from classogdf_1_1_v_comparer
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
E = TypeVar('E')

class VComparer(Generic[E]):

	"""Abstract base class for comparer classes."""

	def __init__(self) -> None:
		"""Initializes a comparer."""
		...

	def __destruct__(self) -> None:
		...

	def compare(self, x : E, y : E) -> int:
		"""Comparesxandyand returns the result as an integer."""
		...

	def equal(self, x : E, y : E) -> bool:
		"""Returns true iffx=y."""
		...

	def geq(self, x : E, y : E) -> bool:
		"""Returns true iffx>=y."""
		...

	def greater(self, x : E, y : E) -> bool:
		"""Returns true iffx>y."""
		...

	def leq(self, x : E, y : E) -> bool:
		"""Returns true iffx<=y."""
		...

	def less(self, x : E, y : E) -> bool:
		"""Returns true iffx<y."""
		...
