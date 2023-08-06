# file stubs/ogdf/dot/Lexer.py generated from classogdf_1_1dot_1_1_lexer
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
class Lexer(object):

	"""Lexical analysis tool."""

	def __init__(self, input : std.istream) -> None:
		"""Initializes lexer with given input (but does nothing to it)."""
		...

	def __destruct__(self) -> None:
		...

	def tokenize(self) -> bool:
		"""Scans input and turns it into token list."""
		...

	def tokens(self) -> List[Token]:
		"""Returns list of tokens (first useLexer::tokenize())"""
		...
