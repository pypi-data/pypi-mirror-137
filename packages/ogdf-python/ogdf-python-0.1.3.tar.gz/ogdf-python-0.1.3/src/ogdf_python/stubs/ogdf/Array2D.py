# file stubs/ogdf/Array2D.py generated from classogdf_1_1_array2_d
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
E = TypeVar('E')

class Array2D(Generic[E]):

	"""The parameterized classArray2Dimplements dynamic two-dimensional arrays."""

	@overload
	def __init__(self) -> None:
		"""Creates a two-dimensional array with empty index set."""
		...

	@overload
	def __init__(self, A : Array2D[ E ]) -> None:
		"""Creates a two-dimensional array containing the elements ofA(move semantics)."""
		...

	@overload
	def __init__(self, A : Array2D[ E ]) -> None:
		"""Creates a two-dimensional array that is a copy ofA."""
		...

	@overload
	def __init__(self, a : int, b : int, c : int, d : int) -> None:
		"""Creates a two-dimensional array with index set [a, ...,b]*[c, ...,d]."""
		...

	@overload
	def __init__(self, a : int, b : int, c : int, d : int, x : E) -> None:
		"""Creates a two-dimensional array with index set [a, ...,b]*[c, ...,d] and initailizes all elements withx."""
		...

	def __destruct__(self) -> None:
		"""Destructor."""
		...

	def det(self) -> float:
		"""Returns the determinant of the matrix."""
		...

	def fill(self, x : E) -> None:
		"""Sets all elements tox."""
		...

	def high1(self) -> int:
		"""Returns the maximal array index in dimension 1."""
		...

	def high2(self) -> int:
		"""Returns the maximal array index in dimension 2."""
		...

	@overload
	def init(self) -> None:
		"""Reinitializes the array to an array with empty index set."""
		...

	@overload
	def init(self, a : int, b : int, c : int, d : int) -> None:
		"""Reinitializes the array to an array with index set [a, ...,b]*[c, ...,d]."""
		...

	@overload
	def init(self, a : int, b : int, c : int, d : int, x : E) -> None:
		"""Reinitializes the array to an array with index set [a, ...,b]*[c, ...,d] and initializes all entries withx."""
		...

	def low1(self) -> int:
		"""Returns the minimal array index in dimension 1."""
		...

	def low2(self) -> int:
		"""Returns the minimal array index in dimension 2."""
		...

	@overload
	def __call__(self, i : int, j : int) -> E:
		"""Returns a reference to the element with index (i,j)."""
		...

	@overload
	def __call__(self, i : int, j : int) -> E:
		"""Returns a reference to the element with index (i,j)."""
		...

	@overload
	def __assign__(self, A : Array2D[ E ]) -> Array2D[ E ]:
		"""Assignment operator (move semantics)."""
		...

	@overload
	def __assign__(self, array2 : Array2D[ E ]) -> Array2D[ E ]:
		"""Assignment operator."""
		...

	def size(self) -> int:
		"""Returns the size (number of elements) of the array."""
		...

	def size1(self) -> int:
		"""Returns the length of the index interval (number of entries) in dimension 1."""
		...

	def size2(self) -> int:
		"""Returns the length of the index interval (number of entries) in dimension 2."""
		...
