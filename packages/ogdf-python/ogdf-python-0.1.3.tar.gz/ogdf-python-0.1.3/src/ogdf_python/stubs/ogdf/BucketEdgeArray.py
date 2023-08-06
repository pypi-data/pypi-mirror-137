# file stubs/ogdf/BucketEdgeArray.py generated from classogdf_1_1_bucket_edge_array
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
class BucketEdgeArray(ogdf.BucketFunc[ edge ]):

	"""Bucket function for edges."""

	def __init__(self, edgeArray : EdgeArray[  int ]) -> None:
		"""Constructs a bucket function."""
		...

	def getBucket(self, e : edge) -> int:
		"""Returns bucket of edgee."""
		...
