# file stubs/ogdf/fast_multipole_embedder/RandomNodeSet.py generated from classogdf_1_1fast__multipole__embedder_1_1_random_node_set
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
class RandomNodeSet(object):

	"""utility class to select multiple nodes randomly"""

	def __init__(self, G : Graph) -> None:
		"""init the random node set with the given graph. takes O(n)"""
		...

	def __destruct__(self) -> None:
		"""destructor"""
		...

	def chooseNode(self) -> node:
		"""chooses a node from the available nodes in O(1)"""
		...

	def isAvailable(self, v : node) -> bool:
		...

	def nodesLeft(self) -> int:
		"""number of nodes available"""
		...

	def removeNode(self, v : node) -> None:
		"""removes a node from available nodes (assumes v is available) in O(1)"""
		...
