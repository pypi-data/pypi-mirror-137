# file stubs/ogdf/ClusterGraphCopy.py generated from classogdf_1_1_cluster_graph_copy
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
class ClusterGraphCopy(ogdf.ClusterGraph):

	@overload
	def __init__(self) -> None:
		...

	@overload
	def __init__(self, H : ExtendedNestingGraph, CG : ClusterGraph) -> None:
		...

	def copy(self, cOrig : cluster) -> cluster:
		...

	def getOriginalClusterGraph(self) -> ClusterGraph:
		...

	def init(self, H : ExtendedNestingGraph, CG : ClusterGraph) -> None:
		...

	def original(self, cCopy : cluster) -> cluster:
		...

	def setParent(self, v : node, c : cluster) -> None:
		...
