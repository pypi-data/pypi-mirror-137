# file stubs/ogdf/G6AbstractReaderWithAdjacencyMatrix.py generated from classogdf_1_1_g6_abstract_reader_with_adjacency_matrix
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
Implementation = TypeVar('Implementation')

class G6AbstractReaderWithAdjacencyMatrix(ogdf.G6AbstractReader[ Implementation ], Generic[Implementation]):

	"""Common abstract base class for g6 formats based on adjacency matrix (graph6/digraph6)"""

	def parseByteBody(self, byte : int) -> bool:
		"""Called for every read byte in the graph body."""
		...

	def __init__(self, G : Graph, _is : std.istream, forceHeader : bool) -> None:
		...

	def finishedRow(self) -> bool:
		"""Checks whether our current adjacency matrix row inreaderis complete."""
		...

	def tryAddEdge(self, add : bool) -> None:
		"""Adds an edge ifaddis true. In any case, increase internal matrix indices inreader."""
		...
