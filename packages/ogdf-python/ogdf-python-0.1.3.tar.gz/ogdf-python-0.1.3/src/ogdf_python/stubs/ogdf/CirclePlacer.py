# file stubs/ogdf/CirclePlacer.py generated from classogdf_1_1_circle_placer
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
class CirclePlacer(ogdf.InitialPlacer):

	"""The circle placer for multilevel layout."""

	class NodeSelection(enum.Enum):

		New = enum.auto()

		Old = enum.auto()

		All = enum.auto()

	def __init__(self) -> None:
		...

	def placeOneLevel(self, MLG : MultilevelGraph) -> None:
		...

	def setCircleSize(self, sizeIncrease : float) -> None:
		...

	def setNodeSelection(self, nodeSel : NodeSelection) -> None:
		...

	def setRadiusFixed(self, fixed : bool) -> None:
		...
