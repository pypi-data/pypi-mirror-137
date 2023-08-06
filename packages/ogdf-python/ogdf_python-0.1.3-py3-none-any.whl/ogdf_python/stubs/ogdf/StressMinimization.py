# file stubs/ogdf/StressMinimization.py generated from classogdf_1_1_stress_minimization
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
class StressMinimization(ogdf.LayoutModule):

	"""Energy-based layout using stress minimization."""

	class TerminationCriterion(enum.Enum):

		_None = enum.auto()

		PositionDifference = enum.auto()

		Stress = enum.auto()

	def __init__(self) -> None:
		"""Constructor: Constructs instance of stress majorization."""
		...

	def __destruct__(self) -> None:
		"""Destructor."""
		...

	def call(self, GA : GraphAttributes) -> None:
		"""Calls the layout algorithm with uniform edge costs."""
		...

	def convergenceCriterion(self, criterion : TerminationCriterion) -> None:
		"""Tells which TerminationCriterion should be used."""
		...

	def fixXCoordinates(self, fix : bool) -> None:
		"""Tells whether the x coordinates are allowed to be modified or not."""
		...

	def fixYCoordinates(self, fix : bool) -> None:
		"""Tells whether the y coordinates are allowed to be modified or not."""
		...

	def fixZCoordinates(self, fix : bool) -> None:
		"""Tells whether the z coordinates are allowed to be modified or not."""
		...

	def hasInitialLayout(self, hasInitialLayout : bool) -> None:
		"""Tells whether the current layout should be used or the initial layout needs to be computed."""
		...

	def layoutComponentsSeparately(self, separate : bool) -> None:
		"""Sets whether the graph's components should be layouted separately or a dummy distance should be used for nodes within different components."""
		...

	def setEdgeCosts(self, edgeCosts : float) -> None:
		"""Sets the desired distance between adjacent nodes. If the new value is smaller or equal 0 the default value (100) is used."""
		...

	def setIterations(self, numberOfIterations : int) -> None:
		"""Sets a fixed number of iterations for stress majorization. If the new value is smaller or equal 0 the default value (200) is used."""
		...

	def useEdgeCostsAttribute(self, useEdgeCostsAttribute : bool) -> None:
		"""Tells whether the edge costs are uniform or defined by some edge costs attribute."""
		...
