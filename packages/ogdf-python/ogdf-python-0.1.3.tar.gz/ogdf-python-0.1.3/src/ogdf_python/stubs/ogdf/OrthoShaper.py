# file stubs/ogdf/OrthoShaper.py generated from classogdf_1_1_ortho_shaper
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
class OrthoShaper(object):

	class NetworkNodeType(enum.Enum):

		"""Types of network nodes: nodes and faces."""

		low = enum.auto()

		high = enum.auto()

		inner = enum.auto()

		outer = enum.auto()

	def __init__(self) -> None:
		...

	def __destruct__(self) -> None:
		...

	@overload
	def align(self) -> bool:
		...

	@overload
	def align(self, al : bool) -> None:
		...

	@overload
	def call(self, PG : PlanRep, E : CombinatorialEmbedding, OR : OrthoRep, fourPlanar : bool = True) -> None:
		...

	@overload
	def call(self, PG : PlanRepUML, E : CombinatorialEmbedding, OR : OrthoRep, fourPlanar : bool = True) -> None:
		...

	@overload
	def distributeEdges(self) -> bool:
		...

	@overload
	def distributeEdges(self, b : bool) -> None:
		...

	@overload
	def fixDegreeFourAngles(self) -> bool:
		...

	@overload
	def fixDegreeFourAngles(self, b : bool) -> None:
		...

	def getBendBound(self) -> int:
		...

	@overload
	def multiAlign(self) -> bool:
		...

	@overload
	def multiAlign(self, b : bool) -> None:
		...

	def setBendBound(self, i : int) -> None:
		"""Set bound for number of bends per edge (none if set to 0). If shape flow computation is unsuccessful, the bound is increased iteratively."""
		...

	def setDefaultSettings(self) -> None:
		...

	@overload
	def traditional(self) -> bool:
		...

	@overload
	def traditional(self, b : bool) -> None:
		...
