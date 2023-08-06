# file stubs/ogdf/Tuple2.py generated from classogdf_1_1_tuple2
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
E2 = TypeVar('E2')

E1 = TypeVar('E1')

class Tuple2(Generic[E1, E2]):

	"""Tuples of two elements (2-tuples)."""

	#: The first element.
	m_x1 : E1 = ...

	#: The second element.
	m_x2 : E2 = ...

	@overload
	def __init__(self) -> None:
		"""Constructs a 2-tuple using default constructors."""
		...

	@overload
	def __init__(self, y1 : E1, y2 : E2) -> None:
		"""Constructs a 2-tuple for given values."""
		...

	@overload
	def __init__(self, t2 : Tuple2[ E1, E2 ]) -> None:
		"""Constructs a 2-tuple that is a copy oft2."""
		...

	def __assign__(self, _ : Tuple2[ E1, E2 ]) -> Tuple2:
		...

	@overload
	def x1(self) -> E1:
		"""Returns a reference the first element."""
		...

	@overload
	def x1(self) -> E1:
		"""Returns a reference the first element."""
		...

	@overload
	def x2(self) -> E2:
		"""Returns a reference the second element."""
		...

	@overload
	def x2(self) -> E2:
		"""Returns a reference the second element."""
		...
