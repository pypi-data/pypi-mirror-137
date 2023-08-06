# file stubs/ogdf/ClusterSetSimple.py generated from classogdf_1_1_cluster_set_simple
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
class ClusterSetSimple(object):

	"""Simple cluster sets."""

	def __init__(self, C : ClusterGraph) -> None:
		"""Creates an empty cluster set associated with clustered graphC."""
		...

	def __destruct__(self) -> None:
		...

	def clear(self) -> None:
		"""Removes all clusters fromS."""
		...

	def clusters(self) -> SListPure[cluster]:
		"""Returns a reference to the list of clusters contained inS."""
		...

	def insert(self, c : cluster) -> None:
		"""Inserts clustercintoS."""
		...

	def isMember(self, c : cluster) -> bool:
		"""Returns true if clustercis contained inS, false otherwise."""
		...
