# file stubs/ogdf/HashFuncTuple.py generated from classogdf_1_1_hash_func_tuple
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
Hash2_ = TypeVar('Hash2_')

K2_ = TypeVar('K2_')

Hash1_ = TypeVar('Hash1_')

K1_ = TypeVar('K1_')

class HashFuncTuple(Generic[K1_, K2_, Hash1_, Hash2_]):

	@overload
	def __init__(self) -> None:
		...

	@overload
	def __init__(self, hash1 : Hash1_, hash2 : Hash2_) -> None:
		...

	def hash(self, key : Tuple2[ K1_, K2_ ]) -> size_t:
		...
