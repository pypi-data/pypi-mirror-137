# file stubs/ogdf/QType.py generated from structogdf_1_1_q_type
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
class QType(object):

	m_limit : int = ...

	m_start : adjEntry = ...

	@overload
	def __init__(self) -> None:
		...

	@overload
	def __init__(self, adj : adjEntry, i : int) -> None:
		...
