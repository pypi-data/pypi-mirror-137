# file stubs/ogdf/LibraryNotSupportedException.py generated from classogdf_1_1_library_not_supported_exception
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
class LibraryNotSupportedException(ogdf.Exception):

	"""Exception thrown when an external library shall be used which is not supported."""

	@overload
	def __init__(self, file : str = None, line : int = -1) -> None:
		"""Constructs a library not supported exception."""
		...

	@overload
	def __init__(self, code : LibraryNotSupportedCode, file : str = None, line : int = -1) -> None:
		"""Constructs a library not supported exception."""
		...

	def exceptionCode(self) -> LibraryNotSupportedCode:
		"""Returns the error code of the exception."""
		...
