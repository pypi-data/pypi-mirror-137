# file stubs/ogdf/HashArray2D.py generated from classogdf_1_1_hash_array2_d
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
H1 = TypeVar('H1')

I1 = TypeVar('I1')

I2 = TypeVar('I2')

H2 = TypeVar('H2')

E = TypeVar('E')

class HashArray2D(ogdf.Hashing[ Tuple2[ I1, I2 ], E, HashFuncTuple[ I1, I2, DefHashFunc[ I1 ], DefHashFunc[ I2 ] ] ], Generic[I1, I2, E, H1, H2]):

	"""Indexed 2-dimensional arrays using hashing for element access."""

	#: The type of const-iterators for 2D-hash arrays.
	const_iterator : Type = HashConstIterator2D[ I1, I2, E, H1, H2 ]

	@overload
	def __init__(self) -> None:
		"""Creates a 2D-hash array."""
		...

	@overload
	def __init__(self, defaultValue : E, hashFunc1 : H1 = H1(), hashFunc2 : H2 = H2()) -> None:
		"""Creates a 2D-hash array and sets the default value todefaultValue."""
		...

	@overload
	def __init__(self, A : HashArray2D[ I1, I2, E, H1, H2 ]) -> None:
		"""Copy constructor."""
		...

	def __destruct__(self) -> None:
		...

	def begin(self) -> HashConstIterator2D[ I1, I2, E, H1, H2 ]:
		"""Returns an iterator pointing to the first element."""
		...

	def clear(self) -> None:
		"""Undefines all indices."""
		...

	def empty(self) -> int:
		"""Returns if any indices are defined."""
		...

	def isDefined(self, i : I1, j : I2) -> bool:
		"""Returns true iff entry (i,j) is defined."""
		...

	@overload
	def __call__(self, i : I1, j : I2) -> E:
		"""Returns a reference to entry (i,j)."""
		...

	@overload
	def __call__(self, i : I1, j : I2) -> E:
		"""Returns a const reference to entry (i,j)."""
		...

	def __assign__(self, A : HashArray2D[ I1, I2, E, H1, H2 ]) -> HashArray2D:
		"""Assignment operator."""
		...

	def size(self) -> int:
		"""Returns the number of defined elements in the table."""
		...

	def undefine(self, i : I1, j : I2) -> None:
		"""Undefines the entry at index (i,j)."""
		...
