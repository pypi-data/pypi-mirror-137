# file stubs/ogdf/BoothLueker.py generated from classogdf_1_1_booth_lueker
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
class BoothLueker(ogdf.PlanarityModule):

	"""Booth-Lueker planarity test."""

	def __init__(self) -> None:
		...

	def __destruct__(self) -> None:
		...

	def isPlanar(self, G : Graph) -> bool:
		"""Returns true, if G is planar, false otherwise."""
		...

	def isPlanarDestructive(self, G : Graph) -> bool:
		"""Returns true, if G is planar, false otherwise."""
		...

	def planarEmbed(self, G : Graph) -> bool:
		"""Returns true, if G is planar, false otherwise. If true, G contains a planar embedding."""
		...

	def planarEmbedPlanarGraph(self, G : Graph) -> bool:
		"""Returns true, if G is planar, false otherwise. If true, G contains a planar embedding."""
		...
