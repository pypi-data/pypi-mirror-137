# file stubs/ogdf/SolarPlacer.py generated from classogdf_1_1_solar_placer
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
class SolarPlacer(ogdf.InitialPlacer):

	"""The solar placer for multilevel layout."""

	def placeOneLevel(self, MLG : MultilevelGraph) -> None:
		...
