# file stubs/ogdf/fast_multipole_embedder/LQPartitioner.py generated from classogdf_1_1fast__multipole__embedder_1_1_l_q_partitioner
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
class LQPartitioner(object):

	"""The partitioner which partitions the quadtree into subtrees and partitions the sequence of inner nodes and leaves."""

	def __init__(self, pLocalContext : FMELocalContext) -> None:
		...

	def currPartition(self) -> FMETreePartition:
		...

	@overload
	def newPartition(self) -> None:
		...

	@overload
	def newPartition(self, nodeID : int) -> None:
		...

	def partition(self) -> None:
		...

	def partitionNodeChains(self) -> None:
		...
