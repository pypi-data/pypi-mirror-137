# file stubs/ogdf/SpringEmbedderFRExact/__init__.py generated from classogdf_1_1_spring_embedder_f_r_exact
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
class SpringEmbedderFRExact(ogdf.ForceLayoutModule):

	"""Fruchterman-Reingold algorithm with (exact) layout."""

	class CoolingFunction(enum.Enum):

		Factor = enum.auto()

		Logarithmic = enum.auto()

	def __init__(self) -> None:
		"""Creates an instance of Fruchterman/Reingold (exact) layout."""
		...

	def call(self, GA : GraphAttributes) -> None:
		"""Calls the layout algorithm for graph attributesGA."""
		...

	@overload
	def checkConvergence(self) -> bool:
		...

	@overload
	def checkConvergence(self, b : bool) -> None:
		...

	def convTolerance(self, tol : float) -> None:
		...

	@overload
	def coolingFunction(self) -> CoolingFunction:
		"""Returns the current setting for the cooling function."""
		...

	@overload
	def coolingFunction(self, f : CoolingFunction) -> None:
		"""Sets the parameter coolingFunction tof."""
		...

	@overload
	def idealEdgeLength(self) -> float:
		"""Returns the ideal edge length."""
		...

	@overload
	def idealEdgeLength(self, len : float) -> None:
		"""Sets the ideal edge length tolen."""
		...

	@overload
	def iterations(self) -> int:
		"""Returns the current setting of iterations."""
		...

	@overload
	def iterations(self, i : int) -> None:
		"""Sets the number of iterations toi."""
		...

	@overload
	def minDistCC(self) -> float:
		"""Returns the minimum distance between connected components."""
		...

	@overload
	def minDistCC(self, x : float) -> None:
		"""Sets the minimum distance between connected components tox."""
		...

	def nodeWeights(self, on : bool) -> None:
		"""Switches use of node weights given in GraphAttributtes."""
		...

	@overload
	def noise(self) -> bool:
		"""Returns the current setting of nodes."""
		...

	@overload
	def noise(self, on : bool) -> None:
		"""Sets the parameter noise toon."""
		...

	@overload
	def pageRatio(self) -> float:
		"""Returns the page ratio."""
		...

	@overload
	def pageRatio(self, x : float) -> None:
		"""Sets the page ration tox."""
		...
