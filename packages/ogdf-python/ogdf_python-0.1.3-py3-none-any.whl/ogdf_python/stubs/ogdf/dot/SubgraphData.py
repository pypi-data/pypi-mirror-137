# file stubs/ogdf/dot/SubgraphData.py generated from structogdf_1_1dot_1_1_subgraph_data
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
class SubgraphData(object):

	"""A helper structure containing information for recursive graph reading."""

	edgeDefaults : List[Ast.AttrList] = ...

	nodeDefaults : List[Ast.AttrList] = ...

	nodes : std.set[node] = ...

	rootCluster : cluster = ...

	def __init__(self, root : cluster, nodeDefaultsVector : List[Ast.AttrList], edgeDefaultsVector : List[Ast.AttrList], nodeSet : std.set[node]) -> None:
		"""Initializes structure with given data."""
		...

	def withCluster(self, newRootCluster : cluster) -> SubgraphData:
		"""Returns almost the same structure, but with root cluster."""
		...

	def withDefaults(self, newNodeDefaults : List[Ast.AttrList], newEdgeDefaults : List[Ast.AttrList]) -> SubgraphData:
		"""Returns almost the same structure, but with new defaults."""
		...

	def withNodes(self, newNodes : std.set[node]) -> SubgraphData:
		"""Returns almost the same structure, but with new node list."""
		...
