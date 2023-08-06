# file stubs/ogdf/Matching.py generated from namespaceogdf_1_1_matching
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
EdgeContainer = TypeVar('EdgeContainer')

class Matching(object):

	"""Simple algorithms for matchings."""

	def findMaximalMatching(self, graph : Graph, matching : ArrayBuffer[edge]) -> None:
		"""Obtains a maximal matching in O(|E|) time."""
		...

	def isMatching(self, graph : Graph, matching : EdgeContainer) -> bool:
		"""Checks in time O(|V| + size ofmatching) if the given set of edges represents a matching."""
		...

	@overload
	def isMaximal(self, graph : Graph, matching : EdgeContainer) -> bool:
		"""Checks in time O(|E|) if there are edges that could be added tomatching."""
		...

	@overload
	def isMaximal(self, graph : Graph, matching : EdgeContainer, addable : edge) -> bool:
		"""Checks in time O(|E|) if there are edges that could be added tomatching."""
		...

	def isMaximalMatching(self, graph : Graph, matching : EdgeContainer) -> bool:
		"""Checks in O(|V| + |E|) time ifmatchingis a maximal matching."""
		...

	def isPerfect(self, graph : Graph, matching : EdgeContainer) -> bool:
		"""Checks in O(1) ifmatching(assuming it is a matching and the graph is simple and connected) is perfect."""
		...

	def isPerfectMatching(self, graph : Graph, matching : EdgeContainer) -> bool:
		"""Checks in O(|V| + size ofmatching) ifmatchingis a perfect matching."""
		...
