# file stubs/ogdf/PQNodeKey.py generated from classogdf_1_1_p_q_node_key
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
Y = TypeVar('Y')

T = TypeVar('T')

X = TypeVar('X')

class PQNodeKey(Generic[T, X, Y]):

	"""The class templatePQNodeKeyis a derived class of class templatePQBasicKey."""

	#: Stores the information. Has to be overloaded by the client.
	m_userStructInfo : X = ...

	def __init__(self, info : X) -> None:
		...

	def __destruct__(self) -> None:
		...

	def userStructInfo(self) -> X:
		"""Returnsm_userStructInfo."""
		...

	def userStructInternal(self) -> Y:
		"""Returns 0."""
		...

	def userStructKey(self) -> T:
		"""Returns 0."""
		...
