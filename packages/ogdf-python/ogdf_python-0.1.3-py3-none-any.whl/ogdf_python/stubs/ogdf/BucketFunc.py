# file stubs/ogdf/BucketFunc.py generated from classogdf_1_1_bucket_func
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
E = TypeVar('E')

class BucketFunc(Generic[E]):

	"""Abstract base class for bucket functions."""

	def __destruct__(self) -> None:
		...

	def getBucket(self, x : E) -> int:
		"""Returns the bucket ofx."""
		...
