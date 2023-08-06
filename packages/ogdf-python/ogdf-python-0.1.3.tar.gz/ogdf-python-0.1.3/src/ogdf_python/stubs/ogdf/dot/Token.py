# file stubs/ogdf/dot/Token.py generated from structogdf_1_1dot_1_1_token
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
class Token(object):

	"""Just a simple token struct representing a DOT file fragment."""

	class Type(enum.Enum):

		assignment = enum.auto()

		colon = enum.auto()

		semicolon = enum.auto()

		comma = enum.auto()

		edgeOpDirected = enum.auto()

		edgeOpUndirected = enum.auto()

		leftBracket = enum.auto()

		rightBracket = enum.auto()

		leftBrace = enum.auto()

		rightBrace = enum.auto()

		graph = enum.auto()

		digraph = enum.auto()

		subgraph = enum.auto()

		node = enum.auto()

		edge = enum.auto()

		strict = enum.auto()

		identifier = enum.auto()

	#: Indicated a token column.
	column : size_t = ...

	#: Indicates a token row (line).
	row : size_t = ...

	#: The type of an field.
	type : Type = ...

	#: Identifier content (nullptr for non-id tokens).
	value : str = ...

	def __init__(self, tokenRow : size_t, tokenColumn : size_t, identifierContent : str = None) -> None:
		...

	def toString(self, type : Type) -> str:
		"""Returns string representation of given token type."""
		...
