# file stubs/ogdf/Graph6Reader.py generated from classogdf_1_1_graph6_reader
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
class Graph6Reader(ogdf.G6AbstractReaderWithAdjacencyMatrix[ Graph6Implementation ]):

	def __init__(self, G : Graph, _is : std.istream, forceHeader : bool) -> None:
		...
