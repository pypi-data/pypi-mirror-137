# file stubs/ogdf/RandomPlacer.py generated from classogdf_1_1_random_placer
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
class RandomPlacer(ogdf.InitialPlacer):

	"""The random placer for multilevel layout."""

	def __init__(self) -> None:
		...

	def placeOneLevel(self, MLG : MultilevelGraph) -> None:
		...

	def setCircleSize(self, factor : float) -> None:
		...
