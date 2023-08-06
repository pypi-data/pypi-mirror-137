# file stubs/ogdf/davidson_harel/Planarity/__init__.py generated from classogdf_1_1davidson__harel_1_1_planarity
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
class Planarity(ogdf.davidson_harel.EnergyFunction):

	def __init__(self, AG : GraphAttributes) -> None:
		"""Initializes data structures to speed up later computations."""
		...

	def __destruct__(self) -> None:
		...

	def computeEnergy(self) -> None:
		"""Computes energy of initial layout and stores it inm_energy."""
		...
