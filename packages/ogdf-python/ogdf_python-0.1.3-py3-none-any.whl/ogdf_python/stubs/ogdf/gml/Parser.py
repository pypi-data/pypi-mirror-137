# file stubs/ogdf/gml/Parser.py generated from classogdf_1_1gml_1_1_parser
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
class Parser(object):

	"""Reads GML file and constructs GML parse tree."""

	def __init__(self, _is : std.istream, doCheck : bool = False) -> None:
		...

	def __destruct__(self) -> None:
		"""Destruction: destroys object tree."""
		...

	def error(self) -> bool:
		...

	@overload
	def read(self, G : Graph) -> bool:
		...

	@overload
	def read(self, G : Graph, GA : GraphAttributes) -> bool:
		...

	def readCluster(self, G : Graph, CG : ClusterGraph, ACG : ClusterGraphAttributes = None) -> bool:
		...

	def recursiveClusterRead(self, clusterObject : Object, CG : ClusterGraph, c : cluster, ACG : ClusterGraphAttributes = None) -> bool:
		"""Reads cluster subtree information recursively."""
		...
