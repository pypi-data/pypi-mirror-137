# file stubs/ogdf/HashConstIterator2D.py generated from classogdf_1_1_hash_const_iterator2_d
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
I1_ = TypeVar('I1_')

Hash2_ = TypeVar('Hash2_')

I2_ = TypeVar('I2_')

Hash1_ = TypeVar('Hash1_')

E_ = TypeVar('E_')

class HashConstIterator2D(ogdf.HashConstIterator[ Tuple2[ I1_, I2_ ], E_, HashFuncTuple[ I1_, I2_, DefHashFunc[ I1_ ], DefHashFunc[ I2_ ] ] ], Generic[I1_, I2_, E_, Hash1_, Hash2_]):

	"""Const-iterator for 2D-hash arrays."""

	@overload
	def __init__(self) -> None:
		"""Creates an (invalid) iterator."""
		...

	@overload
	def __init__(self, it : HashConstIterator2D[ I1_, I2_, E_, Hash1_, Hash2_ ]) -> None:
		"""Copy constructor."""
		...

	@overload
	def __init__(self, it : HashConstIterator[Tuple2[ I1_, I2_ ], E_,HashFuncTuple[ I1_, I2_, Hash1_, Hash2_ ] ]) -> None:
		"""Copy constructor (fromHashConstIterator)."""
		...

	def info(self) -> E_:
		"""Returns the information of the element pointed to."""
		...

	def key1(self) -> I1_:
		"""Returns the first key of the hash element pointed to."""
		...

	def key2(self) -> I2_:
		"""Returns the second key of the hash element pointed to."""
		...

	def __preinc__(self) -> HashConstIterator2D[ I1_, I2_, E_, Hash1_, Hash2_ ]:
		"""Sets the iterator to the next element in the 2D-hash array."""
		...

	def __assign__(self, it : HashConstIterator2D[ I1_, I2_, E_, Hash1_, Hash2_ ]) -> HashConstIterator2D[ I1_, I2_, E_, Hash1_, Hash2_ ]:
		"""Assignemnt operator."""
		...

	def valid(self) -> bool:
		"""Returns true iff the iterator points to an element."""
		...
