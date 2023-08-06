# file stubs/ogdf/PlanarSubgraphModule.py generated from classogdf_1_1_planar_subgraph_module
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
TCost = TypeVar('TCost')

class PlanarSubgraphModule(ogdf.Module, ogdf.Timeouter, Generic[TCost]):

	"""Interface for planar subgraph algorithms."""

	def __init__(self) -> None:
		"""Initializes a planar subgraph module (default constructor)."""
		...

	@overload
	def call(self, G : Graph, cost : EdgeArray[ TCost ], preferredEdges : List[edge], delEdges : List[edge], preferredImplyPlanar : bool = False) -> ReturnType:
		"""Returns the set of edgesdelEdgeswhich have to be deleted to obtain the planar subgraph."""
		...

	@overload
	def call(self, G : Graph, cost : EdgeArray[ TCost ], delEdges : List[edge]) -> ReturnType:
		"""Returns the set of edgesdelEdgeswhich have to be deleted to obtain the planar subgraph."""
		...

	@overload
	def call(self, G : Graph, preferredEdges : List[edge], delEdges : List[edge], preferredImplyPlanar : bool = False) -> ReturnType:
		"""Returns the set of edgesdelEdgeswhich have to be deleted to obtain the planar subgraph."""
		...

	@overload
	def call(self, G : Graph, delEdges : List[edge]) -> ReturnType:
		"""Returns the set of edgesdelEdgeswhich have to be deleted to obtain the planar subgraph."""
		...

	@overload
	def callAndDelete(self, GC : GraphCopy, preferredEdges : List[edge], delOrigEdges : List[edge], preferredImplyPlanar : bool = False) -> ReturnType:
		"""MakesGCplanar by deleting edges."""
		...

	@overload
	def callAndDelete(self, GC : GraphCopy, delOrigEdges : List[edge]) -> ReturnType:
		"""MakesGplanar by deleting edges."""
		...

	def clone(self) -> PlanarSubgraphModule:
		"""Returns a new instance of the planar subgraph module with the same option settings."""
		...

	@overload
	def maxThreads(self) -> int:
		"""Returns the maximal number of used threads."""
		...

	@overload
	def maxThreads(self, n : int) -> None:
		"""Sets the maximal number of used threads ton."""
		...

	@overload
	def __call__(self, G : Graph, preferredEdges : List[edge], delEdges : List[edge], preferredImplyPlanar : bool = False) -> ReturnType:
		"""Returns the set of edgesdelEdgeswhich have to be deleted to obtain the planar subgraph."""
		...

	@overload
	def __call__(self, G : Graph, delEdges : List[edge]) -> ReturnType:
		"""Returns the set of edgesdelEdgeswhich have to be deleted to obtain the planar subgraph."""
		...

	def doCall(self, G : Graph, preferredEdges : List[edge], delEdges : List[edge], pCost : EdgeArray[ TCost ] = None, preferredImplyPlanar : bool = False) -> ReturnType:
		"""Computes the set of edgesdelEdgeswhich have to be deleted to obtain the planar subgraph."""
		...
