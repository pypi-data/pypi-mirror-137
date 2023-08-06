# file stubs/ogdf/LCA.py generated from classogdf_1_1_l_c_a
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
class LCA(object):

	"""Implements the <O(nlogn), O(1)>-time "sparse table" algorithm by Bender and Farach-Colton to compute lowest common ancestors (LCAs) in arborescences (notarbitrary directed acyclic graphs)."""

	def __init__(self, G : Graph, root : node = None) -> None:
		"""Builds the LCA data structure for an arborescence."""
		...

	def call(self, u : node, v : node) -> node:
		"""Returns the LCA of two nodesuandv."""
		...

	def level(self, v : node) -> int:
		"""Returns the level of a node. The level of the root is 0."""
		...
