# file stubs/ogdf/PQLeafKey.py generated from classogdf_1_1_p_q_leaf_key
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
Y = TypeVar('Y')

T = TypeVar('T')

X = TypeVar('X')

class PQLeafKey(ogdf.PQBasicKey[ T, X, Y ], Generic[T, X, Y]):

	"""The class templatePQLeafKeyis a derived class of class templatePQBasicKey."""

	#: Them_userStructKeyhas to be overloaded by the client.
	m_userStructKey : T = ...

	def __init__(self, element : T) -> None:
		...

	def __destruct__(self) -> None:
		...

	def userStructInfo(self) -> X:
		"""Returns 0."""
		...

	def userStructInternal(self) -> Y:
		"""Returns 0."""
		...

	def userStructKey(self) -> T:
		"""Returnsm_userStructKey."""
		...
