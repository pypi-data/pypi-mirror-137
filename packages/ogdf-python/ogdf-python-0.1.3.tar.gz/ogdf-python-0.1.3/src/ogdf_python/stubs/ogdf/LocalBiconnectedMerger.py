# file stubs/ogdf/LocalBiconnectedMerger.py generated from classogdf_1_1_local_biconnected_merger
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
class LocalBiconnectedMerger(ogdf.MultilevelBuilder):

	"""The local biconnected merger for multilevel layout."""

	def __init__(self) -> None:
		"""Constructs aLocalBiconnectedMergermultilevel builder."""
		...

	def setFactor(self, factor : float) -> None:
		"""Specifies the ratio between two consecutive level sizes up to which merging is done."""
		...
