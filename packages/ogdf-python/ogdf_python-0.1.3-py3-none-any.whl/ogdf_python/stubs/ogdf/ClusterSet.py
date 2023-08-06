# file stubs/ogdf/ClusterSet.py generated from classogdf_1_1_cluster_set
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
class ClusterSet(object):

	"""Cluster sets."""

	def __init__(self, C : ClusterGraph) -> None:
		"""Creates an empty cluster set associated with clustered graphC."""
		...

	def __destruct__(self) -> None:
		...

	def clear(self) -> None:
		"""Removes all clusters fromS."""
		...

	def clusters(self) -> List[cluster]:
		"""Returns a reference to the list of clusters contained inS."""
		...

	def insert(self, c : cluster) -> None:
		"""Inserts clustercintoS."""
		...

	def isMember(self, c : cluster) -> bool:
		"""Returns true if clustercis contained inS, false otherwise."""
		...

	def remove(self, c : cluster) -> None:
		"""Removes clustercfromS."""
		...

	def size(self) -> int:
		"""Returns the size ofS."""
		...
