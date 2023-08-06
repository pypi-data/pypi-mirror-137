# file stubs/ogdf/G6AbstractInstance.py generated from classogdf_1_1_g6_abstract_instance
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
Implementation = TypeVar('Implementation')

class G6AbstractInstance(Generic[Implementation]):

	"""Abstract base class for reader/writer instances."""

	c_asciishift : int = ...

	#: File format specification.
	m_implementation : Implementation = ...

	def __init__(self) -> None:
		...

	def __destruct__(self) -> None:
		...
