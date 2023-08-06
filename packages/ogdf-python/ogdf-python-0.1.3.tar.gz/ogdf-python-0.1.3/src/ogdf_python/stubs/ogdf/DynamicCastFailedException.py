# file stubs/ogdf/DynamicCastFailedException.py generated from classogdf_1_1_dynamic_cast_failed_exception
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
class DynamicCastFailedException(ogdf.Exception):

	"""Exception thrown when result of cast is 0."""

	def __init__(self, file : str = None, line : int = -1) -> None:
		"""Constructs a dynamic cast failed exception."""
		...
