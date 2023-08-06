# file stubs/ogdf/BitonicOrdering.py generated from classogdf_1_1_bitonic_ordering
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
class BitonicOrdering(object):

	def __init__(self, G : Graph, adj_st_edge : adjEntry) -> None:
		...

	def getIndex(self, v : node) -> int:
		...

	def getNode(self, i : int) -> node:
		...
