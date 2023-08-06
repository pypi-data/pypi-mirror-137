# file stubs/ogdf/ScalingLayout.py generated from classogdf_1_1_scaling_layout
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
class ScalingLayout(ogdf.MultilevelLayoutModule):

	"""Scales a graph layout and calls a secondary layout algorithm."""

	class ScalingType(enum.Enum):

		"""To define the relative scale used for aGraph, the ScalingType is applied."""

		#: Scales by a factor relative to the drawing.
		RelativeToDrawing = enum.auto()

		#: Scales by a factor relative to the avg edge weights to be used in combination with the fixed edge length setting inModularMultilevelMixer.
		RelativeToAvgLength = enum.auto()

		#: Scales by a factor relative to the desired Edgelength m_desEdgeLength.
		RelativeToDesiredLength = enum.auto()

		#: Absolute factor, can be used to scale relative to level size change.
		Absolute = enum.auto()

	def __init__(self) -> None:
		...

	@overload
	def call(self, GA : GraphAttributes) -> None:
		"""Computes a layout of graphGA."""
		...

	@overload
	def call(self, GA : GraphAttributes) -> None:
		"""Computes a layout of graphGA."""
		...

	@overload
	def call(self, MLG : MultilevelGraph) -> None:
		"""Computes a layout of graphMLG."""
		...

	@overload
	def call(self, MLG : MultilevelGraph) -> None:
		"""Computes a layout of graphMLG."""
		...

	def setDesiredEdgeLength(self, eLength : float) -> None:
		...

	def setExtraScalingSteps(self, steps : int) -> None:
		"""Sets how often the scaling should be repeated."""
		...

	def setLayoutRepeats(self, repeats : int) -> None:
		"""Sets how often theLayoutModuleshould be applied."""
		...

	def setMMM(self, mmm : ModularMultilevelMixer) -> None:
		"""Is used to compute the scaling relatively to the level size change when ScalingType st_absolute is used."""
		...

	def setScaling(self, min : float, max : float) -> None:
		"""Sets the minimum and the maximum scaling factor."""
		...

	def setScalingType(self, type : ScalingType) -> None:
		"""Sets a ScalingType wich sets the relative scale for theGraph."""
		...

	def setSecondaryLayout(self, layout : LayoutModule) -> None:
		"""Sets aLayoutModulethat should be applied after scaling."""
		...
