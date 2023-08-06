# file stubs/ogdf/NoStdComparerException.py generated from classogdf_1_1_no_std_comparer_exception
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
class NoStdComparerException(ogdf.Exception):

	"""Exception thrown when a required standard comparer has not been specialized."""

	def __init__(self, file : str = None, line : int = -1) -> None:
		"""Constructs a no standard comparer available exception."""
		...
