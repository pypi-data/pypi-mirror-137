# file stubs/ogdf/MinSteinerTreeMehlhorn/MehlhornTripleBucketMinFunc.py generated from classogdf_1_1_min_steiner_tree_mehlhorn_1_1_mehlhorn_triple_bucket_min_func
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
class MehlhornTripleBucketMinFunc(ogdf.BucketFunc[ MehlhornTriple ]):

	"""Helper class to sort MehlhornTriples lexicographically."""

	def __init__(self) -> None:
		...

	def getBucket(self, MT : MehlhornTriple) -> int:
		...
