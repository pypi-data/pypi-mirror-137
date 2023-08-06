# file stubs/ogdf/MedianPlacer.py generated from classogdf_1_1_median_placer
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
class MedianPlacer(ogdf.InitialPlacer):

	"""The median placer for multilevel layout."""

	def placeOneLevel(self, MLG : MultilevelGraph) -> None:
		...
