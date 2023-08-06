# file stubs/ogdf/Math/internal.py generated from namespaceogdf_1_1_math_1_1internal
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
T = TypeVar('T')

size = TypeVar('size')

class internal(object):

	@overload
	def nextPower2(self, x : T) -> Annotated[ T , "std.enable_if[ size==1, T ].type"]:
		...

	@overload
	def nextPower2(self, x : T) -> Annotated[ T , "std.enable_if[ size !=1, T ].type"]:
		"""Efficiently computes the next power of 2 without branching. See "Hacker's Delight" 2nd Edition, by Henry S. Warren, Fig. 3.3."""
		...
