# file stubs/ogdf/pq_internal/Compare.py generated from classogdf_1_1pq__internal_1_1_compare
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
C = TypeVar('C')

T = TypeVar('T')

class Compare(Generic[T, C]):

	"""Used to compare elements with assigned priorities."""

	@overload
	def __init__(self, compare : C = C()) -> None:
		...

	@overload
	def __init__(self, other : Compare) -> None:
		...

	def __call__(self, x : T, y : T) -> bool:
		...
