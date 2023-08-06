# file stubs/ogdf/pq_internal/PairTemplate.py generated from classogdf_1_1pq__internal_1_1_pair_template
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
P = TypeVar('P')

E = TypeVar('E')

class PairTemplate(Generic[E, P]):

	"""Pair for storing an element and a priority."""

	@overload
	def __init__(self) -> None:
		...

	@overload
	def __init__(self, element : E, priority : P) -> None:
		...

	def element(self) -> E:
		...

	def priority(self) -> P:
		...
