# file stubs/ogdf/ConvexHull.py generated from classogdf_1_1_convex_hull
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
class ConvexHull(object):

	"""Computes the convex hull of a set of points or a layout."""

	def __init__(self) -> None:
		...

	def __destruct__(self) -> None:
		...

	def calcNormal(self, start : DPoint, end : DPoint) -> DPoint:
		...

	@overload
	def call(self, GA : GraphAttributes) -> DPolygon:
		...

	@overload
	def call(self, MLG : MultilevelGraph) -> DPolygon:
		...

	@overload
	def call(self, points : List[DPoint]) -> DPolygon:
		...

	def leftOfLine(self, normal : DPoint, point : DPoint, pointOnLine : DPoint) -> float:
		...
