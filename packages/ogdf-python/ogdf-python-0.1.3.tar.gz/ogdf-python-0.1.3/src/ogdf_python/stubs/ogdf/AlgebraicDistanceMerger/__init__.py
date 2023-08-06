# file stubs/ogdf/AlgebraicDistanceMerger/__init__.py generated from classogdf_1_1_algebraic_distance_merger
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
class AlgebraicDistanceMerger(ogdf.MultilevelBuilder):

	def __init__(self) -> None:
		...

	def levelSizeFactor(self) -> float:
		...

	def setLevelSizeFactor(self, f : float) -> None:
		...

	def buildOneLevel(self, MLG : MultilevelGraph) -> bool:
		"""This method constructs one more level on top of an existingMultilevelGraph."""
		...
