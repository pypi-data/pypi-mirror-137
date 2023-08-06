# file stubs/ogdf/EpsilonTest.py generated from classogdf_1_1_epsilon_test
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
T = TypeVar('T')

class EpsilonTest(object):

	def __init__(self, epsilon : float = 1.0e-8) -> None:
		"""Constructs anEpsilonTestwith a given epsilon (double) for comparisons."""
		...

	@overload
	def equal(self, x : T, y : T) -> Annotated[ bool , "std.enable_if[ std.is_integral[ T ].value, bool ].type"]:
		"""Compare if x is EQUAL to y for integral types."""
		...

	@overload
	def equal(self, x : T, y : T) -> Annotated[ bool , "std.enable_if[ std.is_floating_point[ T ].value, bool ].type"]:
		"""Compare if x is EQUAL to y for floating point types, using the given epsilon."""
		...

	@overload
	def geq(self, x : T, y : T) -> Annotated[ bool , "std.enable_if[ std.is_integral[ T ].value, bool ].type"]:
		"""Compare if x is GEQ to y for integral types."""
		...

	@overload
	def geq(self, x : T, y : T) -> Annotated[ bool , "std.enable_if[ std.is_floating_point[ T ].value, bool ].type"]:
		"""Compare if x is GEQ to y for floating point types, using the given epsilon."""
		...

	@overload
	def greater(self, x : T, y : T) -> Annotated[ bool , "std.enable_if[ std.is_integral[ T ].value, bool ].type"]:
		"""Compare if x is GREATER than y for integral types."""
		...

	@overload
	def greater(self, x : T, y : T) -> Annotated[ bool , "std.enable_if[ std.is_floating_point[ T ].value, bool ].type"]:
		"""Compare if x is GREATER than y for floating point types, using the given epsilon."""
		...

	@overload
	def leq(self, x : T, y : T) -> Annotated[ bool , "std.enable_if[ std.is_integral[ T ].value, bool ].type"]:
		"""Compare if x is LEQ than y for integral types."""
		...

	@overload
	def leq(self, x : T, y : T) -> Annotated[ bool , "std.enable_if[ std.is_floating_point[ T ].value, bool ].type"]:
		"""Compare if x is LEQ than y for floating point types, using the given epsilon."""
		...

	@overload
	def less(self, x : T, y : T) -> Annotated[ bool , "std.enable_if[ std.is_integral[ T ].value, bool ].type"]:
		"""Compare if x is LESS than y for integral types."""
		...

	@overload
	def less(self, x : T, y : T) -> Annotated[ bool , "std.enable_if[ std.is_floating_point[ T ].value, bool ].type"]:
		"""Compare if x is LESS than y for floating point types, using the given epsilon."""
		...
