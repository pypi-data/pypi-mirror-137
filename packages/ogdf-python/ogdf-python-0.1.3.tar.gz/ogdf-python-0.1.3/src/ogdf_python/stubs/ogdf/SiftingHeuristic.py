# file stubs/ogdf/SiftingHeuristic.py generated from classogdf_1_1_sifting_heuristic
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
class SiftingHeuristic(ogdf.LayerByLayerSweep):

	"""The sifting heuristic for 2-layer crossing minimization."""

	class Strategy(enum.Enum):

		"""Enumerates the different sifting strategies."""

		LeftToRight = enum.auto()

		DescDegree = enum.auto()

		Random = enum.auto()

	@overload
	def __init__(self) -> None:
		"""Creates a new instance of the sifting heuristic with default option settings."""
		...

	@overload
	def __init__(self, crossMin : SiftingHeuristic) -> None:
		"""Creates a new instance of the sifting heuristic with the same option settings ascrossMin."""
		...

	def __destruct__(self) -> None:
		...

	def call(self, L : Level) -> None:
		"""Calls the sifting heuristic for levelL."""
		...

	def cleanup(self) -> None:
		"""Does some clean-up after calls."""
		...

	def clone(self) -> LayerByLayerSweep:
		"""Returns a new instance of the sifting heuristic with the same option settings."""
		...

	def init(self, levels : HierarchyLevels) -> None:
		"""Initializes crossing minimization for hierarchyH."""
		...

	@overload
	def strategy(self) -> Strategy:
		"""Get for Strategy."""
		...

	@overload
	def strategy(self, strategy : Strategy) -> None:
		"""Set for Strategy."""
		...
