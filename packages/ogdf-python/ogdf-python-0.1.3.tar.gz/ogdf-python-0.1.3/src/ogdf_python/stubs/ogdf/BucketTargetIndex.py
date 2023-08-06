# file stubs/ogdf/BucketTargetIndex.py generated from classogdf_1_1_bucket_target_index
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
class BucketTargetIndex(ogdf.BucketFunc[ edge ]):

	"""Bucket function using the index of an edge's target node as bucket."""

	def getBucket(self, e : edge) -> int:
		"""Returns target index ofe."""
		...
