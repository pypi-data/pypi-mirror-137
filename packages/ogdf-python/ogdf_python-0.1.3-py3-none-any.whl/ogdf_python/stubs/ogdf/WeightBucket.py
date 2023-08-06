# file stubs/ogdf/WeightBucket.py generated from classogdf_1_1_weight_bucket
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
class WeightBucket(ogdf.BucketFunc[ node ]):

	def __init__(self, pWeight : NodeArray[  int ]) -> None:
		...

	def getBucket(self, x : node) -> int:
		"""Returns the bucket ofx."""
		...
