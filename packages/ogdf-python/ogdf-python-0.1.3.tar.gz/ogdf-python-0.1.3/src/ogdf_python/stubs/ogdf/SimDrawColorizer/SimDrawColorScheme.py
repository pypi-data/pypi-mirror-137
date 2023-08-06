# file stubs/ogdf/SimDrawColorizer/SimDrawColorScheme.py generated from classogdf_1_1_sim_draw_colorizer_1_1_sim_draw_color_scheme
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
class SimDrawColorScheme(object):

	"""Manages the various color schemes."""

	def __init__(self, colorScm : colorScheme, numberOfGraphs : int) -> None:
		"""constructor"""
		...

	def __destruct__(self) -> None:
		"""destructor"""
		...

	def assignColScm(self, numberOfGraphs : int) -> None:
		"""sets the color component arrays according to colorschemeXS"""
		...

	def getColor(self, subGraphBits : int, numberOfGraphs : int) -> Color:
		"""joins the different color components together"""
		...
