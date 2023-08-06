# file stubs/ogdf/embedding_inserter/CrossingsBucket.py generated from classogdf_1_1embedding__inserter_1_1_crossings_bucket
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
PLANREP = TypeVar('PLANREP')

class CrossingsBucket(ogdf.BucketFunc[ edge ], Generic[PLANREP]):

	"""Bucket function for sorting edges by decreasing number of crossings."""

	def __init__(self, pPG : PLANREP) -> None:
		...

	def getBucket(self, x : edge) -> int:
		"""Returns the bucket ofx."""
		...
