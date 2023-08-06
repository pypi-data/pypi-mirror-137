# file stubs/ogdf/fast_multipole_embedder/BinCoeff.py generated from classogdf_1_1fast__multipole__embedder_1_1_bin_coeff
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
TYP = TypeVar('TYP')

class BinCoeff(Generic[TYP]):

	"""binomial coeffs from Hachuls FMMM"""

	def __init__(self, n : int) -> None:
		...

	def __destruct__(self) -> None:
		...

	def free_array(self) -> None:
		"""Free space for BK."""
		...

	def init_array(self) -> None:
		"""Init BK -matrix for values n, k in 0 to t."""
		...

	def value(self, n : int, k : int) -> TYP:
		...
