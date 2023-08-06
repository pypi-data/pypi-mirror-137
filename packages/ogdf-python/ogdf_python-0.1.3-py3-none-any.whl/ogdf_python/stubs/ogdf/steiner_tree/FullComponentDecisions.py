# file stubs/ogdf/steiner_tree/FullComponentDecisions.py generated from structogdf_1_1steiner__tree_1_1_full_component_decisions
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
class FullComponentDecisions(object):

	"""Contains rules of thumb to decide which (sub-)algorithms to use for the generation of full components."""

	def computeDensity(self, n : int, m : int) -> float:
		"""Computes the ratio of edges to potential edges in a simple graph."""
		...

	def shouldUseAllNodeDijkstra(self, n : int, m : int) -> bool:
		"""Returns true iff the rule of thumb predicts to callDijkstraon all nodes instead of the algorithm by Floyd."""
		...

	def shouldUseAllTerminalDijkstra(self, n : int, m : int, t : int) -> bool:
		"""Returns true iff the rule of thumb predicts to callDijkstraon all terminals instead of the algorithm by Floyd."""
		...

	def shouldUseDijkstra(self, k : int, n : int, m : int, t : int) -> bool:
		"""Returns true iff the rule of thumb predicts to use multipleDijkstracalls instead of the algorithm by Floyd."""
		...

	def shouldUseErickson(self, n : int, m : int) -> bool:
		"""Returns true iff the rule of thumb predicts to use the algorithm by Erickson et al instead of the Dreyfus-Wagner algorithm."""
		...
