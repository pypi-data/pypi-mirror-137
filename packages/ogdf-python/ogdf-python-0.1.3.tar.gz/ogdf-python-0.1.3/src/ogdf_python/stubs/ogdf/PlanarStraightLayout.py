# file stubs/ogdf/PlanarStraightLayout.py generated from classogdf_1_1_planar_straight_layout
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
class PlanarStraightLayout(ogdf.PlanarGridLayoutModule):

	"""Implementation of the Planar-Straight layout algorithm."""

	# Optional parameters

	@overload
	def sizeOptimization(self) -> bool:
		"""Returns the current setting of option sizeOptimization."""
		...

	@overload
	def sizeOptimization(self, opt : bool) -> None:
		"""Sets the option sizeOptimization toopt."""
		...

	@overload
	def baseRatio(self) -> float:
		"""Returns the current setting of option baseRatio."""
		...

	@overload
	def baseRatio(self, ratio : float) -> None:
		"""Sets the option baseRatio toratio."""
		...

	# Module options

	def setAugmenter(self, pAugmenter : AugmentationModule) -> None:
		"""Sets the augmentation module."""
		...

	def setShellingOrder(self, pOrder : ShellingOrderModule) -> None:
		"""Sets the shelling order module."""
		...

	def setEmbedder(self, pEmbedder : EmbedderModule) -> None:
		"""Sets the module option for the graph embedding algorithm."""
		...

	def __init__(self) -> None:
		"""Constructs an instance of the Planar-Straight layout algorithm."""
		...

	def __destruct__(self) -> None:
		...
