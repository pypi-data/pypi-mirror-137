# file stubs/ogdf/DavidsonHarel.py generated from classogdf_1_1_davidson_harel
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
class DavidsonHarel(object):

	"""The Davidson-Harel approach for drawing graphs."""

	def __init__(self) -> None:
		"""Creates an instance of Davidsen-Harel base class."""
		...

	def __destruct__(self) -> None:
		...

	def addEnergyFunction(self, F : EnergyFunction, weight : float) -> None:
		"""Adds an energy functionFwith a certain weight."""
		...

	def call(self, GA : GraphAttributes) -> None:
		"""Calls the Davidson-Harel method for graphGA."""
		...

	def returnEnergyFunctionNames(self) -> List[ str ]:
		"""Returns a list of the names of the energy functions."""
		...

	def returnEnergyFunctionWeights(self) -> List[ float ]:
		"""Returns a list of the weights of the energy functions."""
		...

	def setNumberOfIterations(self, steps : int) -> None:
		"""Sets the number of iterations for each temperature step tosteps."""
		...

	def setStartTemperature(self, startTemp : int) -> None:
		"""Sets the start temperature tostartTemp."""
		...
