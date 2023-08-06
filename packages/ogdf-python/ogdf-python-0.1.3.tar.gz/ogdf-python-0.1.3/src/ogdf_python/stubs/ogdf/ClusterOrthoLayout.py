# file stubs/ogdf/ClusterOrthoLayout.py generated from classogdf_1_1_cluster_ortho_layout
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
class ClusterOrthoLayout(ogdf.LayoutClusterPlanRepModule):

	"""Represents a planar orthogonal drawing algorithm for c-planar, c-connected clustered graphs."""

	def __init__(self) -> None:
		"""Initializes an instance of classClusterOrthoLayout."""
		...

	def align(self, b : bool) -> None:
		"""Sets alignment option."""
		...

	@overload
	def call(self, PG : ClusterPlanRep, adjExternal : adjEntry, drawing : Layout) -> None:
		"""Calls planar UML layout algorithm."""
		...

	@overload
	def call(self, PG : ClusterPlanRep, adjExternal : adjEntry, drawing : Layout, origEdges : List[edge], originalGraph : Graph) -> None:
		"""Call method for non c-planar graphs."""
		...

	@overload
	def costAssoc(self) -> int:
		"""Returns cost of associations which is used in the compactions step."""
		...

	@overload
	def costAssoc(self, c : int) -> None:
		"""Sets cost of associations which is used in the compactions step."""
		...

	@overload
	def costGen(self) -> int:
		"""Returns cost of generalizations."""
		...

	@overload
	def costGen(self, c : int) -> None:
		"""Sets cost of generalizations."""
		...

	@overload
	def cOverhang(self) -> float:
		"""Returns cOverhang, where cOverhang * separation defines the minimum."""
		...

	@overload
	def cOverhang(self, c : float) -> None:
		"""Sets cOverhang value."""
		...

	@overload
	def margin(self) -> float:
		"""Returns the distance from the tight bounding box to the boundary of the drawing."""
		...

	@overload
	def margin(self, m : float) -> None:
		"""Sets the distance from the tight bounding box to the boundary of the drawing."""
		...

	def optionProfile(self, i : int) -> None:
		"""Sets the option profile, thereby fixing a set of drawing options."""
		...

	@overload
	def preferedDir(self) -> OrthoDir:
		"""Returns the preferred direction of generalizations."""
		...

	@overload
	def preferedDir(self, dir : OrthoDir) -> None:
		"""Sets the preferred direction of generalizations."""
		...

	def scaling(self, b : bool) -> None:
		"""Sets scaling option for compaction step."""
		...

	@overload
	def separation(self) -> float:
		"""Returns the minimum distance between edges and vertices."""
		...

	@overload
	def separation(self, sep : float) -> None:
		"""Sets the minimum distance between edges and vertices."""
		...

	def setOptions(self, optionField : int) -> None:
		"""Sets generic options by setting field bits."""
		...
