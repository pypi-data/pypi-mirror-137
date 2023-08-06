# file stubs/ogdf/AcyclicSubgraphModule.py generated from classogdf_1_1_acyclic_subgraph_module
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
class AcyclicSubgraphModule(object):

	"""Base class of algorithms for computing a maximal acyclic subgraph."""

	def __init__(self) -> None:
		"""Initializes an acyclic subgraph module."""
		...

	def __destruct__(self) -> None:
		"""Destruction."""
		...

	def call(self, G : Graph, arcSet : List[edge]) -> None:
		"""Computes the set of edgesarcSetwhich have to be removed for obtaining an acyclic subgraph ofG."""
		...

	def callAndDelete(self, G : Graph) -> None:
		"""MakesGacyclic by removing edges."""
		...

	@overload
	def callAndReverse(self, G : Graph) -> None:
		"""MakesGacyclic by reversing edges."""
		...

	@overload
	def callAndReverse(self, G : Graph, reversed : List[edge]) -> None:
		"""MakesGacyclic by reversing edges."""
		...

	def __call__(self, G : Graph, arcSet : List[edge]) -> None:
		"""Computes the set of edgesarcSetwhich have to be removed for obtaining an acyclic subgraph ofG."""
		...
