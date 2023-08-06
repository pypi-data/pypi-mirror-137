# file stubs/ogdf/BucketSourceIndex.py generated from classogdf_1_1_bucket_source_index
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
class BucketSourceIndex(ogdf.BucketFunc[ edge ]):

	"""Bucket function using the index of an edge's source node as bucket."""

	def getBucket(self, e : edge) -> int:
		"""Returns source index ofe."""
		...
