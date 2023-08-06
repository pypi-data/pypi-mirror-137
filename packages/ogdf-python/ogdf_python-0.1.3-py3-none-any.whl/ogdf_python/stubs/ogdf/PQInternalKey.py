# file stubs/ogdf/PQInternalKey.py generated from classogdf_1_1_p_q_internal_key
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
Y = TypeVar('Y')

T = TypeVar('T')

X = TypeVar('X')

class PQInternalKey(ogdf.PQBasicKey[ T, X, Y ], Generic[T, X, Y]):

	"""The class templatePQInternalKeyis a derived class of class templatePQBasicKey."""

	#: The class templatePQInternalKeyhas only one public member: them_userStructInternalthat has to be overloaded by the client.
	m_userStructInternal : Y = ...

	def __init__(self, element : Y) -> None:
		...

	def __destruct__(self) -> None:
		...

	def userStructInfo(self) -> X:
		"""Overloaded pure virtual function returning 0."""
		...

	def userStructInternal(self) -> Y:
		"""Overloaded pure virtual function returningm_userStructInternal."""
		...

	def userStructKey(self) -> T:
		"""Overloaded pure virtual function returning 0."""
		...
