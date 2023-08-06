# file stubs/ogdf/G6Abstract.py generated from classogdf_1_1_g6_abstract
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
class G6Abstract(object):

	"""Abstract base class for implementations."""

	#: The name (header string) of this graph type.
	header : str = ...

	#: The start character for this specific graph type.
	startCharacter : int = ...

	def __init__(self, header_ : str, startCharacter_ : int = static_cast[   int ](0)) -> None:
		...

	def __destruct__(self) -> None:
		...

	def hasStartCharacter(self) -> bool:
		"""Returns true if a start character has been set by the child class."""
		...

	def writeHeader(self, os : std.ostream) -> None:
		"""Writes header information of the child class to a a streamos."""
		...
