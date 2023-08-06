# file stubs/ogdf/MultiEdgeApproxInserter/EmbeddingPreference.py generated from classogdf_1_1_multi_edge_approx_inserter_1_1_embedding_preference
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
class EmbeddingPreference(object):

	class Type(enum.Enum):

		_None = enum.auto()

		RNode = enum.auto()

		PNode = enum.auto()

	s_none : EmbeddingPreference = ...

	@overload
	def __init__(self) -> None:
		...

	@overload
	def __init__(self, a1 : adjEntry, a2 : adjEntry) -> None:
		...

	@overload
	def __init__(self, mirror : bool) -> None:
		...

	def adj1(self) -> adjEntry:
		...

	def adj2(self) -> adjEntry:
		...

	def flip(self) -> None:
		...

	def isNull(self) -> bool:
		...

	def mirror(self) -> bool:
		...

	def print(self, os : std.ostream) -> std.ostream:
		...

	def type(self) -> Type:
		...
