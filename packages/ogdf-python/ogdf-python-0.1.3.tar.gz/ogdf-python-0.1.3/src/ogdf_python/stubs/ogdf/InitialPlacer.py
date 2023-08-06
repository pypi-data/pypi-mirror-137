# file stubs/ogdf/InitialPlacer.py generated from classogdf_1_1_initial_placer
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
class InitialPlacer(object):

	"""Base class for placer modules."""

	m_randomOffset : bool = ...

	def __init__(self) -> None:
		...

	def __destruct__(self) -> None:
		...

	def placeOneLevel(self, MLG : MultilevelGraph) -> None:
		...

	def setRandomOffset(self, on : bool) -> None:
		...
