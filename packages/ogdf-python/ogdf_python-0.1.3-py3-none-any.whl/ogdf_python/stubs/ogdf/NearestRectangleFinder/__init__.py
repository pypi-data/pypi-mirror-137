# file stubs/ogdf/NearestRectangleFinder/__init__.py generated from classogdf_1_1_nearest_rectangle_finder
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
class NearestRectangleFinder(object):

	"""Finds in a given set of rectangles for each point in a given set of points the nearest rectangle."""

	def __init__(self, mad : float = 20, td : float = 5) -> None:
		...

	def find(self, region : Array[RectRegion], point : Array[DPoint], nearest : Array[List[PairRectDist] ]) -> None:
		...

	def findSimple(self, region : Array[RectRegion], point : Array[DPoint], nearest : Array[List[PairRectDist] ]) -> None:
		...

	@overload
	def maxAllowedDistance(self) -> float:
		...

	@overload
	def maxAllowedDistance(self, mad : float) -> None:
		...

	@overload
	def toleranceDistance(self) -> float:
		...

	@overload
	def toleranceDistance(self, td : float) -> None:
		...
