# file stubs/ogdf/IndependentSetMerger.py generated from classogdf_1_1_independent_set_merger
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
class IndependentSetMerger(ogdf.MultilevelBuilder):

	"""The independent set merger for multilevel layout."""

	def __init__(self) -> None:
		...

	def buildAllLevels(self, MLG : MultilevelGraph) -> None:
		...

	def setSearchDepthBase(self, base : float) -> None:
		...
