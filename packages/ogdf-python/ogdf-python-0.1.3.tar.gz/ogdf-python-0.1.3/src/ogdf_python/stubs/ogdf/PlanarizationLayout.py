# file stubs/ogdf/PlanarizationLayout.py generated from classogdf_1_1_planarization_layout
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
class PlanarizationLayout(ogdf.LayoutModule):

	"""The planarization approach for drawing graphs."""

	# Optional parameters

	@overload
	def pageRatio(self) -> float:
		"""Returns the current setting of option pageRatio."""
		...

	@overload
	def pageRatio(self, ratio : float) -> None:
		"""Sets the option pageRatio toratio."""
		...

	@overload
	def minCliqueSize(self) -> int:
		"""Returns the current setting of option minCliqueSize."""
		...

	@overload
	def minCliqueSize(self, i : int) -> None:
		"""Set the option minCliqueSize toi."""
		...

	# Module options

	def setCrossMin(self, pCrossMin : CrossingMinimizationModule) -> None:
		"""Sets the module option for crossing minimization."""
		...

	def setEmbedder(self, pEmbedder : EmbedderModule) -> None:
		"""Sets the module option for the graph embedding algorithm."""
		...

	def setPlanarLayouter(self, pPlanarLayouter : LayoutPlanRepModule) -> None:
		"""Sets the module option for the planar layout algorithm."""
		...

	def setPacker(self, pPacker : CCLayoutPackModule) -> None:
		"""Sets the module option for the arrangement of connected components."""
		...

	# Further information

	def numberOfCrossings(self) -> int:
		"""Returns the number of crossings in the computed layout."""
		...

	def __init__(self) -> None:
		"""Creates an instance of planarization layout and sets options to default values."""
		...

	def __destruct__(self) -> None:
		"""Destructor."""
		...

	@overload
	def call(self, ga : GraphAttributes) -> None:
		"""Calls planarization layout forGraphAttributesga."""
		...

	@overload
	def call(self, ga : GraphAttributes, g : Graph) -> None:
		"""Calls planarization layout with clique handling forGraphAttributesgawith associated graphg."""
		...

	def callSimDraw(self, ga : GraphAttributes) -> None:
		...
