# file stubs/ogdf/InOutPoint.py generated from structogdf_1_1_in_out_point
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
class InOutPoint(object):

	"""Representation of an in- or outpoint."""

	m_adj : adjEntry = ...

	m_dx : int = ...

	m_dy : int = ...

	@overload
	def __init__(self) -> None:
		...

	@overload
	def __init__(self, adj : adjEntry) -> None:
		...
