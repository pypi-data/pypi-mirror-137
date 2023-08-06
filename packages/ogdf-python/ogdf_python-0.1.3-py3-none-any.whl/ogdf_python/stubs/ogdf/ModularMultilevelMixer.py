# file stubs/ogdf/ModularMultilevelMixer.py generated from classogdf_1_1_modular_multilevel_mixer
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
class ModularMultilevelMixer(ogdf.LayoutModule):

	"""Modular multilevel graph layout."""

	class erc(enum.Enum):

		"""Error codes for calls."""

		#: no error
		_None = enum.auto()

		#: level bound exceeded by merger step
		LevelBound = enum.auto()

	def __init__(self) -> None:
		...

	@overload
	def call(self, GA : GraphAttributes) -> None:
		"""Calls the multilevel layout algorithm for graph attributesGA."""
		...

	@overload
	def call(self, MLG : MultilevelGraph) -> None:
		"""Calls the multilevel layout algorithm for multilevel graphMLG."""
		...

	def coarseningRatio(self) -> float:
		"""Returns the ratio c/p between sizes of previous (p) and current (c) level graphs."""
		...

	def errorCode(self) -> erc:
		"""Returns the error code of last call."""
		...

	def setAllEdgeLengths(self, len : float) -> None:
		"""Iflen> 0, all edge weights will be set tolen."""
		...

	def setAllNodeSizes(self, size : float) -> None:
		"""Ifsize> 0, all node sizes will be set tosize."""
		...

	def setFinalLayoutModule(self, finalLayout : LayoutModule) -> None:
		"""Sets the final layout module tofinalLayout."""
		...

	def setInitialPlacer(self, placement : InitialPlacer) -> None:
		"""Sets the initial placer module toplacement."""
		...

	def setLayoutRepeats(self, times : int = 1) -> None:
		"""Determines how many times the one-level layout will be called."""
		...

	def setLevelBound(self, b : bool) -> None:
		"""Determines if computation is stopped when number of levels is too high."""
		...

	def setLevelLayoutModule(self, levelLayout : LayoutModule) -> None:
		"""Sets the one-level layout module tolevelLayout."""
		...

	def setMultilevelBuilder(self, levelBuilder : MultilevelBuilder) -> None:
		"""Sets the multilevel builder module tolevelBuilder."""
		...

	def setRandomize(self, b : bool) -> None:
		"""Determines if an initial random layout is computed."""
		...
