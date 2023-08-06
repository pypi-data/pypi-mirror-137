# file stubs/ogdf/GraphMLParser.py generated from classogdf_1_1_graph_m_l_parser
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
class GraphMLParser(object):

	def __init__(self, _in : std.istream) -> None:
		...

	def __destruct__(self) -> None:
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
