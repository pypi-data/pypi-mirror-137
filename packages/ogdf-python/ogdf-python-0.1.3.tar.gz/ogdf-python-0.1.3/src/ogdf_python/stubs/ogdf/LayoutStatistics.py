# file stubs/ogdf/LayoutStatistics.py generated from classogdf_1_1_layout_statistics
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
class LayoutStatistics(object):

	"""Computes statistical information about a layout."""

	def angles(self, ga : GraphAttributes, considerBends : bool = True) -> ArrayBuffer[ float ]:
		"""Computes the angle for each pair of adjacent edge segments of the layoutga."""
		...

	def edgeLengths(self, ga : GraphAttributes, considerSelfLoops : bool = False) -> ArrayBuffer[ float ]:
		"""Computes the edge length for each edge in the layoutga."""
		...

	def intersectionGraph(self, ga : GraphAttributes, H : Graph, points : NodeArray[DPoint], origNode : NodeArray[node], origEdge : EdgeArray[edge]) -> None:
		"""Computes the intersection graphHof the line segments in the layout given byga."""
		...

	def numberOfBends(self, ga : GraphAttributes, considerSelfLoops : bool = False) -> ArrayBuffer[  int ]:
		"""Computes the number of bends (i.e. bend-points) for each edge in the layoutga."""
		...

	def numberOfCrossings(self, ga : GraphAttributes) -> ArrayBuffer[  int ]:
		"""Computes the number of edge crossings for each edge in the layoutga."""
		...

	def numberOfNodeCrossings(self, ga : GraphAttributes) -> ArrayBuffer[  int ]:
		"""Computes the number of crossings through a non-incident node for each edge in the layoutga."""
		...

	def numberOfNodeOverlaps(self, ga : GraphAttributes) -> ArrayBuffer[  int ]:
		"""Computes the number of node overlaps for each node in the layoutga."""
		...
