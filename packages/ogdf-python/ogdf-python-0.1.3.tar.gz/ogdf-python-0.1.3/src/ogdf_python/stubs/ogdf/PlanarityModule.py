# file stubs/ogdf/PlanarityModule.py generated from classogdf_1_1_planarity_module
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
class PlanarityModule(object):

	"""Module for planarity testing and planar embeddings."""

	def __init__(self) -> None:
		...

	def __destruct__(self) -> None:
		...

	def isPlanar(self, G : Graph) -> bool:
		"""Returns true, if G is planar, false otherwise."""
		...

	def isPlanarDestructive(self, G : Graph) -> bool:
		"""Returns true, if G is planar, false otherwise. In the graph is non-planar, the graph may be arbitrariliy changed after the call."""
		...

	def planarEmbed(self, G : Graph) -> bool:
		"""Returns true, if G is planar, false otherwise. If true, G contains a planar embedding."""
		...

	def planarEmbedPlanarGraph(self, G : Graph) -> bool:
		"""Constructs a planar embedding ofG.Ghasto be planar!"""
		...
