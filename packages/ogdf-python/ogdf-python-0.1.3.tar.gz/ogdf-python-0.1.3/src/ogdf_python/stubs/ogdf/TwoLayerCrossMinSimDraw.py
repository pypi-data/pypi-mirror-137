# file stubs/ogdf/TwoLayerCrossMinSimDraw.py generated from classogdf_1_1_two_layer_cross_min_sim_draw
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
class TwoLayerCrossMinSimDraw(ogdf.LayerByLayerSweep):

	def __init__(self) -> None:
		"""Initializes a two-layer crossing minimization module."""
		...

	@overload
	def call(self, L : Level) -> None:
		"""Performs crossing minimization for levelL."""
		...

	@overload
	def call(self, L : Level, esg : EdgeArray[  int ]) -> None:
		"""Performs crossing minimization for levelL."""
		...

	def clone(self) -> TwoLayerCrossMinSimDraw:
		"""Returns a new instance of the two-layer crossing minimization module with the same option settings."""
		...
