# file stubs/ogdf/RoutingChannel/__init__.py generated from classogdf_1_1_routing_channel
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
ATYPE = TypeVar('ATYPE')

class RoutingChannel(Generic[ATYPE]):

	"""Maintains input sizes for constructive compaction (size of routing channels, separation, cOverhang)"""

	def __init__(self, G : Graph, sep : ATYPE, cOver : float) -> None:
		...

	def computeRoutingChannels(self, OR : OrthoRep, align : bool = False) -> None:
		...

	def cOverhang(self) -> float:
		...

	@overload
	def __call__(self, v : node, dir : OrthoDir) -> ATYPE:
		...

	@overload
	def __call__(self, v : node, dir : OrthoDir) -> ATYPE:
		...

	def overhang(self) -> ATYPE:
		...

	def separation(self) -> ATYPE:
		...
