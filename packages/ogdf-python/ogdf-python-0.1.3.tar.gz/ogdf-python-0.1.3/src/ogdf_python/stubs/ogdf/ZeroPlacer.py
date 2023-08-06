# file stubs/ogdf/ZeroPlacer.py generated from classogdf_1_1_zero_placer
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
class ZeroPlacer(ogdf.InitialPlacer):

	"""The zero placer for multilevel layout."""

	def __init__(self) -> None:
		...

	def placeOneLevel(self, MLG : MultilevelGraph) -> None:
		...

	def setRandomRange(self, range : float) -> None:
		...
