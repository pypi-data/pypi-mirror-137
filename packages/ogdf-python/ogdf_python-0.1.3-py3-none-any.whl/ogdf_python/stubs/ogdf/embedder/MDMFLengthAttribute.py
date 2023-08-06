# file stubs/ogdf/embedder/MDMFLengthAttribute.py generated from classogdf_1_1embedder_1_1_m_d_m_f_length_attribute
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
class MDMFLengthAttribute(object):

	"""Auxiliary length attribute."""

	a : int = ...

	b : int = ...

	@overload
	def __init__(self) -> None:
		"""Default constructor for (0, 0)"""
		...

	@overload
	def __init__(self, x : MDMFLengthAttribute) -> None:
		"""Copy constructor."""
		...

	@overload
	def __init__(self, _a : int, _b : int = 0) -> None:
		"""Converting constructor from int, default second is 0."""
		...

	def __destruct__(self) -> None:
		"""Destructor."""
		...

	def __iadd__(self, x : MDMFLengthAttribute) -> MDMFLengthAttribute:
		...

	def __isub__(self, x : MDMFLengthAttribute) -> MDMFLengthAttribute:
		...

	def __assign__(self, x : MDMFLengthAttribute) -> MDMFLengthAttribute:
		...
