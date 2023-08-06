# file stubs/ogdf/Digraph6Reader.py generated from classogdf_1_1_digraph6_reader
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
class Digraph6Reader(ogdf.G6AbstractReaderWithAdjacencyMatrix[ Digraph6Implementation ]):

	def __init__(self, G : Graph, _is : std.istream, forceHeader : bool) -> None:
		...
