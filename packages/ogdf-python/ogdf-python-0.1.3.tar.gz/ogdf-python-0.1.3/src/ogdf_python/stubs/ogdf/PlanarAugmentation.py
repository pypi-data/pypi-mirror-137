# file stubs/ogdf/PlanarAugmentation.py generated from classogdf_1_1_planar_augmentation
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
class PlanarAugmentation(ogdf.AugmentationModule):

	"""The algorithm for planar biconnectivity augmentation (Mutzel, Fialko)."""

	def __init__(self) -> None:
		"""Creates an instance of the planar augmentation algorithm."""
		...

	def __destruct__(self) -> None:
		"""Destruction."""
		...

	def doCall(self, G : Graph, list : List[edge]) -> None:
		"""The implementation of the algorithm call."""
		...
