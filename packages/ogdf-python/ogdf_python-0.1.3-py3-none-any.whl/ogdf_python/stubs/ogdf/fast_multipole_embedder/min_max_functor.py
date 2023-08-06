# file stubs/ogdf/fast_multipole_embedder/min_max_functor.py generated from structogdf_1_1fast__multipole__embedder_1_1min__max__functor
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
T = TypeVar('T')

class min_max_functor(Generic[T]):

	"""generic min max functor for an array"""

	a : T = ...

	max_value : T = ...

	min_value : T = ...

	def __init__(self, ptr : T, min_var : T, max_var : T) -> None:
		...

	def __call__(self, i : int) -> None:
		...
