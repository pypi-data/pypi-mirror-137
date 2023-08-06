# file stubs/ogdf/BendString.py generated from classogdf_1_1_bend_string
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
class BendString(object):

	"""Represents the bends on an edge e consisting of vertical and horizontal segments."""

	@overload
	def __init__(self) -> None:
		...

	@overload
	def __init__(self, bs : BendString) -> None:
		...

	@overload
	def __init__(self, c : int, n : size_t) -> None:
		...

	@overload
	def __init__(self, bs : BendString) -> None:
		...

	@overload
	def __init__(self, str : str) -> None:
		...

	def __destruct__(self) -> None:
		...

	@overload
	def __iadd__(self, bs : BendString) -> BendString:
		...

	@overload
	def __iadd__(self, str : str) -> BendString:
		...

	@overload
	def __assign__(self, bs : BendString) -> BendString:
		...

	@overload
	def __assign__(self, bs : BendString) -> BendString:
		...

	@overload
	def __getitem__(self, i : size_t) -> int:
		...

	@overload
	def __getitem__(self, i : size_t) -> int:
		...

	@overload
	def set(self) -> None:
		...

	@overload
	def set(self, c : int, n : size_t) -> None:
		...

	@overload
	def set(self, str : str) -> None:
		...

	@overload
	def set(self, obt : OrthoBendType, n : size_t) -> None:
		...

	def size(self) -> size_t:
		...

	def toString(self) -> str:
		...
