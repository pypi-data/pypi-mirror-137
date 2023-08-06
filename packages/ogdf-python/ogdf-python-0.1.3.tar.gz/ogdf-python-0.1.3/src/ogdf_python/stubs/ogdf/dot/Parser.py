# file stubs/ogdf/dot/Parser.py generated from classogdf_1_1dot_1_1_parser
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
class Parser(object):

	"""DOT format parser class."""

	def __init__(self, _in : std.istream) -> None:
		"""Initializes parser class with given input (but does nothing to it)."""
		...

	@overload
	def read(self, G : Graph) -> bool:
		...

	@overload
	def read(self, G : Graph, C : ClusterGraph) -> bool:
		...

	@overload
	def read(self, G : Graph, C : ClusterGraph, CA : ClusterGraphAttributes) -> bool:
		...

	@overload
	def read(self, G : Graph, GA : GraphAttributes) -> bool:
		...

	def requestNode(self, G : Graph, GA : GraphAttributes, C : ClusterGraph, data : SubgraphData, id : str) -> node:
		"""Perfoms a nodequery, returning node for given attribute."""
		...
