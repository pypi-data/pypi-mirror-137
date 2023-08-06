# file stubs/ogdf/OrthoLayout.py generated from classogdf_1_1_ortho_layout
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
class OrthoLayout(ogdf.LayoutPlanRepModule):

	"""The Orthogonal layout algorithm for planar graphs."""

	# Optional parameters

	@overload
	def separation(self) -> float:
		"""Returns the minimum distance between edges and vertices."""
		...

	@overload
	def separation(self, sep : float) -> None:
		"""Sets the minimum distance between vertices."""
		...

	@overload
	def cOverhang(self) -> float:
		"""Returns the optionm_cOverhang, which specifies the minimal distance of incident edges to the corner of a vertex."""
		...

	@overload
	def cOverhang(self, c : float) -> None:
		"""Sets the optionm_cOverhang, which specifies the minimal distance of incident edges to the corner of a vertex."""
		...

	@overload
	def margin(self) -> float:
		"""Returns the desired margin around the drawing."""
		...

	@overload
	def margin(self, m : float) -> None:
		"""Sets the desired margin around the drawing."""
		...

	@overload
	def progressive(self) -> bool:
		"""Returns whether the currently selected orthogonaliaztion model isprogressive."""
		...

	@overload
	def progressive(self, b : bool) -> None:
		"""Selects if the progressive (true) or traditional (false) orthogonalization model is used."""
		...

	@overload
	def scaling(self) -> bool:
		"""Returns whether scaling is used in the compaction phase."""
		...

	@overload
	def scaling(self, b : bool) -> None:
		"""Selects if scaling is used in the compaction phase."""
		...

	def bendBound(self, i : int) -> None:
		"""Set bound on the number of bends."""
		...

	def __init__(self) -> None:
		"""Creates an instance of Orthogonal layout and sets options to default values."""
		...

	def call(self, PG : PlanRep, adjExternal : adjEntry, drawing : Layout) -> None:
		"""Calls the layout algorithm for planarized representationPG."""
		...
