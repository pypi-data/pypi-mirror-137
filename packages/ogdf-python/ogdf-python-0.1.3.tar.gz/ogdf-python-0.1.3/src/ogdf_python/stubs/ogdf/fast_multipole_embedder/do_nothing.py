# file stubs/ogdf/fast_multipole_embedder/do_nothing.py generated from structogdf_1_1fast__multipole__embedder_1_1do__nothing
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
B = TypeVar('B')

A = TypeVar('A')

class do_nothing(object):

	"""the useless do nothing function"""

	@overload
	def __call__(self, a : A) -> None:
		...

	@overload
	def __call__(self, a : A, b : B) -> None:
		...
