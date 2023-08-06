# file stubs/ogdf/steiner_tree/HeavyPathDecomposition.py generated from classogdf_1_1steiner__tree_1_1_heavy_path_decomposition
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
T = TypeVar('T')

class HeavyPathDecomposition(Generic[T]):

	"""An implementation of the heavy path decomposition on trees."""

	def __init__(self, treeEWGraphCopy : EdgeWeightedGraphCopy[ T ]) -> None:
		...

	def getBottleneckSteinerDistance(self, x : node, y : node) -> T:
		"""computes in the bottleneck distance between terminals x and y"""
		...

	def lowestCommonAncestor(self, x : node, y : node) -> node:
		"""computes the lowest common ancestor of nodes x and y using the hpd"""
		...
