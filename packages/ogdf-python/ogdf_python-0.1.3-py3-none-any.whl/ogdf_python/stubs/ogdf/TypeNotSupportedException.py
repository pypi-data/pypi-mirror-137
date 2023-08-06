# file stubs/ogdf/TypeNotSupportedException.py generated from classogdf_1_1_type_not_supported_exception
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
class TypeNotSupportedException(ogdf.Exception):

	"""Exception thrown when a data type is not supported by a generic function."""

	def __init__(self, file : str = None, line : int = -1) -> None:
		"""Constructs a type-not-supported exception."""
		...
