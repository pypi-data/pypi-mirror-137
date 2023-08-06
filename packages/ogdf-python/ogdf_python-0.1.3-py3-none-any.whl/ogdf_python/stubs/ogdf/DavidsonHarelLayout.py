# file stubs/ogdf/DavidsonHarelLayout.py generated from classogdf_1_1_davidson_harel_layout
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
class DavidsonHarelLayout(ogdf.LayoutModule):

	"""The Davidson-Harel layout algorithm."""

	class SettingsParameter(enum.Enum):

		"""Easy way to set fixed costs."""

		Standard = enum.auto()

		Repulse = enum.auto()

		Planar = enum.auto()

	class SpeedParameter(enum.Enum):

		"""Easy way to set temperature and iterations."""

		Fast = enum.auto()

		Medium = enum.auto()

		HQ = enum.auto()

	def __init__(self) -> None:
		"""Creates an instance of Davidson-Harel layout."""
		...

	def __destruct__(self) -> None:
		...

	def call(self, GA : GraphAttributes) -> None:
		"""Calls the layout algorithm for graph attributesGA."""
		...

	def fixSettings(self, sp : SettingsParameter) -> None:
		"""Fixes the cost values to special configurations."""
		...

	def getAttractionWeight(self) -> float:
		"""Returns the weight for the energy functionAttraction."""
		...

	def getNodeOverlapWeight(self) -> float:
		"""Returns the weight for the energy functionNodeOverlap."""
		...

	def getNumberOfIterations(self) -> int:
		"""Returns the number of iterations per temperature step."""
		...

	def getPlanarityWeight(self) -> float:
		"""Returns the weight for the energy functionPlanarity."""
		...

	def getRepulsionWeight(self) -> float:
		"""Returns the weight for the energy functionRepulsion."""
		...

	def getStartTemperature(self) -> int:
		"""Returns the starting temperature."""
		...

	def setAttractionWeight(self, _ : float) -> None:
		"""Sets the weight for the energy functionAttraction."""
		...

	def setIterationNumberAsFactor(self, b : bool) -> None:
		"""Switch between using iteration number as fixed number or factor (*number of nodes of graph)"""
		...

	def setNodeOverlapWeight(self, _ : float) -> None:
		"""Sets the weight for the energy functionNodeOverlap."""
		...

	def setNumberOfIterations(self, steps : int) -> None:
		"""Sets the number of iterations per temperature step tosteps."""
		...

	def setPlanarityWeight(self, _ : float) -> None:
		"""Sets the weight for the energy functionPlanarity."""
		...

	def setPreferredEdgeLength(self, elen : float) -> None:
		"""Sets the preferred edge length toelen."""
		...

	def setPreferredEdgeLengthMultiplier(self, multi : float) -> None:
		"""Sets the preferred edge length multiplier for attraction."""
		...

	def setRepulsionWeight(self, w : float) -> None:
		"""Sets the weight for the energy functionRepulsion."""
		...

	def setSpeed(self, sp : SpeedParameter) -> None:
		"""More convenient way of setting the speed of the algorithm."""
		...

	def setStartTemperature(self, t : int) -> None:
		"""Sets the starting temperature tot."""
		...
