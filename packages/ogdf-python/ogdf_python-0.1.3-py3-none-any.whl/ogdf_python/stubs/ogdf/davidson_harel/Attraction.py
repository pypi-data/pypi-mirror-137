# file stubs/ogdf/davidson_harel/Attraction.py generated from classogdf_1_1davidson__harel_1_1_attraction
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
class Attraction(ogdf.davidson_harel.NodePairEnergy):

	"""Energy function for attraction between two adjacent vertices."""

	def __init__(self, AG : GraphAttributes) -> None:
		...

	def __destruct__(self) -> None:
		...

	def reinitializeEdgeLength(self, multi : float) -> None:
		"""set multiplier for the edge length with repspect to node size to multi"""
		...

	def setPreferredEdgelength(self, length : float) -> None:
		"""set the preferred edge length"""
		...
