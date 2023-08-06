# file stubs/ogdf/LeftistOrdering/__init__.py generated from classogdf_1_1_leftist_ordering
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
class LeftistOrdering(object):

	@overload
	def call(self, G : Graph, adj_v1n : adjEntry, result : List[List[node] ]) -> bool:
		...

	@overload
	def call(self, G : Graph, adj_v1n : adjEntry, partition : Partitioning) -> bool:
		...
