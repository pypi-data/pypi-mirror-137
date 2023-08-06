# file stubs/ogdf/G6AbstractWriter.py generated from classogdf_1_1_g6_abstract_writer
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
Implementation = TypeVar('Implementation')

class G6AbstractWriter(ogdf.G6AbstractInstance[ Implementation ], Generic[Implementation]):

	m_G : Graph = ...

	m_os : std.ostream = ...

	def __init__(self, G : Graph, os : std.ostream) -> None:
		...

	def asciiChar(self, value : int) -> int:
		"""Convert an integervalueto a printable ASCII character."""
		...

	def sixtetChar(self, sixtet : int) -> int:
		"""Convert the nth sixtetsixtetof the number of nodes to a printable ASCII character."""
		...

	def write(self) -> bool:
		"""Execute the write."""
		...

	def writeSize(self, n : int, os : std.ostream) -> None:
		"""Writes the size of the graph to the output stream."""
		...

	def writeBody(self) -> bool:
		...
