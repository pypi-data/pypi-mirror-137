# file stubs/ogdf/LeftistOrdering/Partitioning.py generated from classogdf_1_1_leftist_ordering_1_1_partitioning
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
class Partitioning(object):

	@overload
	def __init__(self) -> None:
		...

	@overload
	def __init__(self, G : Graph, lco : List[List[node] ]) -> None:
		...

	def buildFromResult(self, G : Graph, lco : List[List[node] ]) -> None:
		...

	def getChainAdj(self, k : int, i : int) -> adjEntry:
		...

	def getNode(self, k : int, i : int) -> node:
		...

	def getPathAdj(self, k : int, i : int) -> adjEntry:
		...

	def isSingleton(self, k : int) -> bool:
		...

	def left(self, k : int) -> adjEntry:
		...

	def numNodes(self, k : int) -> int:
		...

	def numPartitions(self) -> int:
		...

	def pathLength(self, k : int) -> int:
		...

	def right(self, k : int) -> adjEntry:
		...
