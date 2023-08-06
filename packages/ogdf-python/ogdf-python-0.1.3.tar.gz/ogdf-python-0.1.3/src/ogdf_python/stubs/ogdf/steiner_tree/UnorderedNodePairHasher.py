# file stubs/ogdf/steiner_tree/UnorderedNodePairHasher.py generated from classogdf_1_1steiner__tree_1_1_unordered_node_pair_hasher
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
class UnorderedNodePairHasher(object):

	"""A class used by the unordered_maps inside the reductions."""

	def __call__(self, v : NodePair) -> int:
		...
