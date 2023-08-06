# file stubs/ogdf/DepthBucket.py generated from classogdf_1_1_depth_bucket
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
class DepthBucket(ogdf.BucketFunc[ node ]):

	@overload
	def __init__(self, _ : DepthBucket) -> None:
		...

	@overload
	def __init__(self, depth : NodeArray[  int ]) -> None:
		...

	def getBucket(self, x : node) -> int:
		"""Returns the bucket ofx."""
		...

	def __assign__(self, _ : DepthBucket) -> DepthBucket:
		...
