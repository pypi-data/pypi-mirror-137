# file stubs/ogdf/InsufficientMemoryException.py generated from classogdf_1_1_insufficient_memory_exception
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
class InsufficientMemoryException(ogdf.Exception):

	"""Exception thrown when not enough memory is available to execute an algorithm."""

	def __init__(self, file : str = None, line : int = -1) -> None:
		"""Constructs an insufficient memory exception."""
		...
