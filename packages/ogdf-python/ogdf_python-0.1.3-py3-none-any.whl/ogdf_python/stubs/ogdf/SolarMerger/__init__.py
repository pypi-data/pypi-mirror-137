# file stubs/ogdf/SolarMerger/__init__.py generated from classogdf_1_1_solar_merger
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
class SolarMerger(ogdf.MultilevelBuilder):

	"""The solar merger for multilevel layout."""

	def __init__(self, simple : bool = False, massAsNodeRadius : bool = False) -> None:
		...

	def buildAllLevels(self, MLG : MultilevelGraph) -> None:
		...
