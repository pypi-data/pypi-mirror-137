# file stubs/ogdf/sse/ComplexDouble.py generated from classogdf_1_1sse_1_1_complex_double
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
class ComplexDouble(object):

	"""Class to generate instrinsics for complex number arithmetic functions."""

	# Standard arithmetic

	def __add__(self, other : ComplexDouble) -> ComplexDouble:
		...

	@overload
	def __sub__(self, other : ComplexDouble) -> ComplexDouble:
		...

	@overload
	def __sub__(self, _ : None) -> ComplexDouble:
		...

	@overload
	def __mul__(self, other : ComplexDouble) -> ComplexDouble:
		...

	@overload
	def operator(self, other : ComplexDouble) -> ComplexDouble:
		...

	@overload
	def __mul__(self, scalar : float) -> ComplexDouble:
		...

	@overload
	def operator(self, scalar : float) -> ComplexDouble:
		...

	@overload
	def __mul__(self, scalar : int) -> ComplexDouble:
		...

	def __iadd__(self, other : ComplexDouble) -> None:
		...

	def __isub__(self, other : ComplexDouble) -> None:
		...

	@overload
	def __imul__(self, other : ComplexDouble) -> None:
		...

	@overload
	def __imul__(self, scalar : float) -> None:
		...

	def __idiv__(self, other : ComplexDouble) -> None:
		...

	# Additional arithmetic

	def length(self) -> float:
		...

	def conj(self) -> ComplexDouble:
		...

	# Assignment

	@overload
	def __assign__(self, other : ComplexDouble) -> ComplexDouble:
		...

	@overload
	def __assign__(self, ptr : float) -> ComplexDouble:
		"""load from 16byte aligned ptr"""
		...

	# LOAD, STORE

	def load(self, ptr : float) -> None:
		"""load from 16byte aligned ptr"""
		...

	def load_unaligned(self, ptr : float) -> None:
		"""load from unaligned ptr"""
		...

	def store(self, ptr : float) -> None:
		"""store to 16byte aligned ptr"""
		...

	def store_unaligned(self, ptr : float) -> None:
		"""store to unaligned ptr"""
		...

	reg : float = ...

	@overload
	def __init__(self) -> None:
		...

	@overload
	def __init__(self, other : ComplexDouble) -> None:
		...

	@overload
	def __init__(self, ptr : float) -> None:
		...

	@overload
	def __init__(self, x : float) -> None:
		...

	@overload
	def __init__(self, x : float, y : float) -> None:
		...
