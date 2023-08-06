# file stubs/ogdf/MixedModelCrossingsBeautifierModule.py generated from classogdf_1_1_mixed_model_crossings_beautifier_module
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
class MixedModelCrossingsBeautifierModule(object):

	"""The base class for Mixed-Model crossings beautifier algorithms."""

	def __init__(self) -> None:
		"""Initializes the Mixed-Model crossings beautifier module."""
		...

	def __destruct__(self) -> None:
		...

	def call(self, PG : PlanRep, gl : GridLayout) -> None:
		...

	def numberOfCrossings(self) -> int:
		"""Returns the number of processed crossings."""
		...

	def doCall(self, PG : PlanRep, gl : GridLayout, L : List[node]) -> None:
		"""Implements the crossings beautifier module."""
		...
