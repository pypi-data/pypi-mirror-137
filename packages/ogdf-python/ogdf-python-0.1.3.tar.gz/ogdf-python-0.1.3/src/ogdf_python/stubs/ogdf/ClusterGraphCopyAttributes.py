# file stubs/ogdf/ClusterGraphCopyAttributes.py generated from classogdf_1_1_cluster_graph_copy_attributes
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
class ClusterGraphCopyAttributes(object):

	"""Manages access on copy of an attributed clustered graph."""

	def __init__(self, H : ExtendedNestingGraph, ACG : ClusterGraphAttributes) -> None:
		"""Initializes instance of classClusterGraphCopyAttributes."""
		...

	def __destruct__(self) -> None:
		...

	def bottom(self, cOrig : cluster) -> float:
		"""Returns coordinate of lower cluster boundary of original clustercOrig."""
		...

	def getClusterGraphAttributes(self) -> ClusterGraphAttributes:
		"""Returns correspondingClusterGraphAttributes."""
		...

	def getHeight(self, v : node) -> float:
		"""Returns height of node v."""
		...

	def getWidth(self, v : node) -> float:
		"""Returns width of node v."""
		...

	def setClusterLeftRight(self, cOrig : cluster, left : float, right : float) -> None:
		...

	def setClusterRect(self, cOrig : cluster, left : float, right : float, top : float, bottom : float) -> None:
		"""Sets the position of the cluster rectangle for original clustercOrig."""
		...

	def setClusterTopBottom(self, cOrig : cluster, top : float, bottom : float) -> None:
		...

	def top(self, cOrig : cluster) -> float:
		"""Returns coordinate of upper cluster boundary of original clustercOrig."""
		...

	def transform(self) -> None:
		"""Sets attributes for the original graph in attributed graph."""
		...

	@overload
	def x(self, v : node) -> float:
		"""Returns reference to x-coord. of node v."""
		...

	@overload
	def x(self, v : node) -> float:
		"""Returns reference to x-coord. of node v."""
		...

	@overload
	def y(self, v : node) -> float:
		"""Returns reference to y-coord. of node v."""
		...

	@overload
	def y(self, v : node) -> float:
		"""Returns reference to y-coord. of node v."""
		...
