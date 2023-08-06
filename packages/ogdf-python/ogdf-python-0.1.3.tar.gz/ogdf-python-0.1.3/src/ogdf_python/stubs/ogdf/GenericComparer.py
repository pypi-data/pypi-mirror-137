# file stubs/ogdf/GenericComparer.py generated from structogdf_1_1_generic_comparer
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
NUM = TypeVar('NUM')

ELEM = TypeVar('ELEM')

ascending = TypeVar('ascending')

class GenericComparer(Generic[ELEM, NUM, ascending]):

	"""Compare elements based on a single comparable attribute."""

	OrderFunction : Type = Callable

	def __init__(self, mapToValue : OrderFunction) -> None:
		"""Construct a comparer with mappingmapToValue."""
		...

	def compare(self, x : ELEM, y : ELEM) -> int:
		"""SeeOGDF_AUGMENT_COMPARER."""
		...
