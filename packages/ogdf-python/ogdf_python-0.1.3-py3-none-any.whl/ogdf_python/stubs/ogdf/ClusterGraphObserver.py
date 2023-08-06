# file stubs/ogdf/ClusterGraphObserver.py generated from classogdf_1_1_cluster_graph_observer
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
class ClusterGraphObserver(object):

	"""Abstract base class for cluster graph observers."""

	m_itCGList : ListIterator[ClusterGraphObserver] = ...

	m_pClusterGraph : ClusterGraph = ...

	@overload
	def __init__(self) -> None:
		...

	@overload
	def __init__(self, CG : ClusterGraph) -> None:
		...

	def __destruct__(self) -> None:
		...

	def clusterAdded(self, v : cluster) -> None:
		...

	def clusterDeleted(self, v : cluster) -> None:
		...

	def getGraph(self) -> ClusterGraph:
		...

	def reregister(self, pCG : ClusterGraph) -> None:
		...
