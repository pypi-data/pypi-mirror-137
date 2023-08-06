# file stubs/ogdf/TargetComparer.py generated from classogdf_1_1_target_comparer
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
STATICCONTENTCOMPARER = TypeVar('STATICCONTENTCOMPARER')

CONTENTTYPE = TypeVar('CONTENTTYPE')

class TargetComparer(Generic[CONTENTTYPE, STATICCONTENTCOMPARER]):

	"""A static comparer which compares the target of pointers ("content"), instead of the pointer's adresses."""

	def equal(self, x : CONTENTPOINTER, y : CONTENTPOINTER) -> bool:
		...

	def geq(self, x : CONTENTPOINTER, y : CONTENTPOINTER) -> bool:
		...

	def greater(self, x : CONTENTPOINTER, y : CONTENTPOINTER) -> bool:
		...

	def leq(self, x : CONTENTPOINTER, y : CONTENTPOINTER) -> bool:
		...

	def less(self, x : CONTENTPOINTER, y : CONTENTPOINTER) -> bool:
		...
