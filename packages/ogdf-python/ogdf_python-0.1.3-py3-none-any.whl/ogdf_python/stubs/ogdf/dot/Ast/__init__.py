# file stubs/ogdf/dot/Ast/__init__.py generated from classogdf_1_1dot_1_1_ast
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
class Ast(object):

	"""DOT format abstract syntax tree class, based on official documentation."""

	def __init__(self, tokens : Tokens) -> None:
		"""Initializes AST building but does not trigger the process itself."""
		...

	def __destruct__(self) -> None:
		...

	def build(self) -> bool:
		"""Builds the DOT format AST."""
		...

	def root(self) -> Graph:
		"""Returns the root of the AST (nullptr if none)."""
		...
