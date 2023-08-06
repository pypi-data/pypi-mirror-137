# file stubs/ogdf/HierarchyClusterLayoutModule.py generated from classogdf_1_1_hierarchy_cluster_layout_module
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
class HierarchyClusterLayoutModule(object):

	"""Interface of hierarchy layout algorithms for cluster graphs."""

	def __init__(self) -> None:
		"""Initializes a hierarchy cluster layout module."""
		...

	def __destruct__(self) -> None:
		...

	def callCluster(self, H : ExtendedNestingGraph, ACG : ClusterGraphAttributes) -> None:
		"""Computes a hierarchy layout of a clustered hierarchyHinACG."""
		...

	def doCall(self, H : ExtendedNestingGraph, ACGC : ClusterGraphCopyAttributes) -> None:
		"""Implements the actual algorithm call."""
		...
