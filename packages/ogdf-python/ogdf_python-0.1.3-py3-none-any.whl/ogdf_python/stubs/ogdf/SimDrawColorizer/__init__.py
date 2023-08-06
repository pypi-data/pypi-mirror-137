# file stubs/ogdf/SimDrawColorizer/__init__.py generated from classogdf_1_1_sim_draw_colorizer
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
class SimDrawColorizer(ogdf.SimDrawManipulatorModule):

	"""Adds color to a graph."""

	class colorScheme(enum.Enum):

		"""types for colorschemes"""

		#: <= 32 different colors
		none = enum.auto()

		#: blue and yellow <= 2 colors
		bluYel = enum.auto()

		#: red and green <= 2 colors
		redGre = enum.auto()

		#: blue and orange <= 2 colors
		bluOra = enum.auto()

		#: teal and purple <= 2 colors
		teaLil = enum.auto()

		#: red, blue and yellow <= 3 colors
		redBluYel = enum.auto()

		#: green, purple and orange <= 3 colors
		greLilOra = enum.auto()

	def __init__(self, SD : SimDraw) -> None:
		"""constructor assigns default color scheme"""
		...

	def addColor(self) -> None:
		"""adds some color to a graph"""
		...

	def addColorNodeVersion(self) -> None:
		"""adds color to a graph including nodes"""
		...

	@overload
	def ColorScheme(self) -> colorScheme:
		"""assigns a new color scheme"""
		...

	@overload
	def ColorScheme(self) -> colorScheme:
		"""returns current color scheme"""
		...
