# file stubs/ogdf/HypernodeElement.py generated from classogdf_1_1_hypernode_element
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
NODELIST = TypeVar('NODELIST')

class HypernodeElement(ogdf.internal.GraphElement):

	"""Class for the representation of hypernodes."""

	class Type(enum.Enum):

		"""The type of hypernodes."""

		normal = enum.auto()

		#: Default type.
		dummy = enum.auto()

		#: Temporary hypernode.
		OR = enum.auto()

		#: Electric circuit: OR gate.
		BUF = enum.auto()

		#: Electric circuit: Buffer gate (iscas85).
		AND = enum.auto()

		#: Electric circuit: AND gate.
		NOR = enum.auto()

		#: Electric circuit: NOR gate.
		NOT = enum.auto()

		#: Electric circuit: NOT gate.
		XOR = enum.auto()

		#: Electric circuit: XOR gate.
		DFF = enum.auto()

		#: Electric circuit: D-Flip-Flop gate (max500nodes).
		NAND = enum.auto()

		#: Electric circuit: NAND gate.
		INPUT = enum.auto()

		#: Electric circuit: Input.
		OUTPUT = enum.auto()

	OGDF_NEW_DELETE = ...

	def adjacent(self, v : hypernode) -> bool:
		"""Returns true iffvis adjacent to the hypernode."""
		...

	def allHyperedges(self, hyperedges : NODELIST) -> None:
		"""Returns a list with all incident hyperedges of the hypernode."""
		...

	def degree(self) -> int:
		"""Returns the hypernode degree."""
		...

	def firstAdj(self) -> adjHypergraphEntry:
		"""Returns the first entry in the adjaceny list."""
		...

	def hypergraph(self) -> Hypergraph:
		"""Returns the hypergraph containing the hypernode."""
		...

	def index(self) -> int:
		"""Returns the (unique) hypernode index."""
		...

	def lastAdj(self) -> adjHypergraphEntry:
		"""Returns the last entry in the adjacency list."""
		...

	def __eq__(self, v : hypernode) -> bool:
		"""Equality operator."""
		...

	def pred(self) -> hypernode:
		"""Returns the predecessor in the list of all hypernodes."""
		...

	def succ(self) -> hypernode:
		"""Returns the successor in the list of all hypernodes."""
		...

	@overload
	def type(self) -> Type:
		"""Returns the type of hypernode."""
		...

	@overload
	def type(self, pType : Type) -> None:
		"""Sets the type of hypernode."""
		...
