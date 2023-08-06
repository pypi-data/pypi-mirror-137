# file stubs/ogdf/AlgorithmFailureException.py generated from classogdf_1_1_algorithm_failure_exception
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
class AlgorithmFailureException(ogdf.Exception):

	"""Exception thrown when an algorithm realizes an internal bug that prevents it from continuing."""

	@overload
	def __init__(self, code : AlgorithmFailureCode, file : str = None, line : int = -1) -> None:
		"""Constructs an algorithm failure exception."""
		...

	@overload
	def __init__(self, file : str = None, line : int = -1) -> None:
		"""Constructs an algorithm failure exception."""
		...

	def exceptionCode(self) -> AlgorithmFailureCode:
		"""Returns the error code of the exception."""
		...
