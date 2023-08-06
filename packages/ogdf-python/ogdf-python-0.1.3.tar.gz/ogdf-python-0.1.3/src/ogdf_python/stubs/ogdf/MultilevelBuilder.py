# file stubs/ogdf/MultilevelBuilder.py generated from classogdf_1_1_multilevel_builder
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
class MultilevelBuilder(object):

	"""Base class for merger modules."""

	m_adjustEdgeLengths : int = ...

	#: stores number of levels for statistics purposes
	m_numLevels : int = ...

	def __init__(self) -> None:
		...

	def __destruct__(self) -> None:
		...

	def buildAllLevels(self, MLG : MultilevelGraph) -> None:
		...

	def getNumLevels(self) -> int:
		...

	def setEdgeLengthAdjustment(self, factor : int) -> None:
		...
