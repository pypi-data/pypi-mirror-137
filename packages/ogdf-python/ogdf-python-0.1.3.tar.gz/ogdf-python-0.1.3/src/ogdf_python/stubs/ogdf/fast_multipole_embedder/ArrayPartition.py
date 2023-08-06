# file stubs/ogdf/fast_multipole_embedder/ArrayPartition.py generated from structogdf_1_1fast__multipole__embedder_1_1_array_partition
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
Func = TypeVar('Func')

class ArrayPartition(object):

	begin : int = ...

	end : int = ...

	def for_loop(self, func : Func) -> None:
		...
