# file stubs/ogdf/Triconnectivity/__init__.py generated from classogdf_1_1_triconnectivity
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
class Triconnectivity(object):

	"""realizes Hopcroft/Tarjan algorithm for finding the triconnected components of a biconnected multi-graph"""

	class CompType(enum.Enum):

		"""type of split-components / triconnected components"""

		bond = enum.auto()

		polygon = enum.auto()

		triconnected = enum.auto()

	#: array of components
	m_component : Array[CompStruct] = ...

	#: number of components
	m_numComp : int = ...

	#: copy of G containing also virtual edges
	m_pGC : GraphCopySimple = ...

	@overload
	def __init__(self, G : Graph) -> None:
		"""Divides G into triconnected components."""
		...

	@overload
	def __init__(self, G : Graph, isTric : bool, s1 : node, s2 : node) -> None:
		"""Tests G for triconnectivity."""
		...

	@overload
	def __init__(self, _ : Triconnectivity) -> None:
		...

	def __destruct__(self) -> None:
		...

	def checkComp(self) -> bool:
		"""Checks if computed triconnected componets are correct."""
		...
