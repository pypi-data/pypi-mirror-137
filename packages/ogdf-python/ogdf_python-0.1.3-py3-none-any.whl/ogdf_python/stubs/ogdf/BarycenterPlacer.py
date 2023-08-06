# file stubs/ogdf/BarycenterPlacer.py generated from classogdf_1_1_barycenter_placer
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
class BarycenterPlacer(ogdf.InitialPlacer):

	"""The barycenter placer for multilevel layout."""

	def __init__(self) -> None:
		...

	def placeOneLevel(self, MLG : MultilevelGraph) -> None:
		...

	def placeOneNode(self, MLG : MultilevelGraph) -> None:
		...

	def weightedPositionPriority(self, on : bool) -> None:
		...
