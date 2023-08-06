# file stubs/ogdf/DfsAcyclicSubgraph.py generated from classogdf_1_1_dfs_acyclic_subgraph
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
class DfsAcyclicSubgraph(ogdf.AcyclicSubgraphModule):

	"""DFS-based algorithm for computing a maximal acyclic subgraph."""

	def call(self, G : Graph, arcSet : List[edge]) -> None:
		"""Computes the set of edgesarcSet, which have to be deleted in the acyclic subgraph."""
		...

	def callUML(self, AG : GraphAttributes, arcSet : List[edge]) -> None:
		"""Call for UML graph."""
		...
