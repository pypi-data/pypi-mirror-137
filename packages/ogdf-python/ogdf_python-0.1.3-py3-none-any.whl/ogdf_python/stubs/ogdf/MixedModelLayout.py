# file stubs/ogdf/MixedModelLayout.py generated from classogdf_1_1_mixed_model_layout
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
class MixedModelLayout(ogdf.GridLayoutPlanRepModule):

	"""Implementation of the Mixed-Model layout algorithm."""

	# Module options

	def setAugmenter(self, pAugmenter : AugmentationModule) -> None:
		"""Sets the augmentation module."""
		...

	def setShellingOrder(self, pOrder : ShellingOrderModule) -> None:
		"""Sets the shelling order module."""
		...

	def setCrossingsBeautifier(self, pBeautifier : MixedModelCrossingsBeautifierModule) -> None:
		"""Sets the crossings beautifier module."""
		...

	def setEmbedder(self, pEmbedder : EmbedderModule) -> None:
		"""Sets the module option for the graph embedding algorithm."""
		...

	def __init__(self) -> None:
		"""Constructs an instance of the Mixed-Model layout algorithm."""
		...

	def __destruct__(self) -> None:
		...

	def doCall(self, PG : PlanRep, adjExternal : adjEntry, gridLayout : GridLayout, boundingBox : IPoint, fixEmbedding : bool) -> None:
		"""Implements the algorithm call."""
		...
