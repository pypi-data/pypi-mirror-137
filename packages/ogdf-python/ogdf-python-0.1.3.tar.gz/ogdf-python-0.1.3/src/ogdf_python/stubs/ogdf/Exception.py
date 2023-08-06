# file stubs/ogdf/Exception.py generated from classogdf_1_1_exception
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
class Exception(object):

	"""Base class of all ogdf exceptions."""

	def __init__(self, file : str = None, line : int = -1) -> None:
		"""Constructs an exception."""
		...

	def file(self) -> str:
		"""Returns the name of the source file where exception was thrown."""
		...

	def line(self) -> int:
		"""Returns the line number where the exception was thrown."""
		...
