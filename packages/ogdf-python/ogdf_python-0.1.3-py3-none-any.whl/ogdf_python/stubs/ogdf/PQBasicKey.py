# file stubs/ogdf/PQBasicKey.py generated from classogdf_1_1_p_q_basic_key
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
Y = TypeVar('Y')

T = TypeVar('T')

X = TypeVar('X')

class PQBasicKey(ogdf.PQBasicKeyRoot, Generic[T, X, Y]):

	def __init__(self) -> None:
		"""Constructor."""
		...

	def nodePointer(self) -> PQNode[ T, X, Y ]:
		"""The functionnodePointer()returns a pointer to an element of typePQNode."""
		...

	def print(self, os : std.ostream) -> std.ostream:
		"""The functionprint()is a virtual function, that can be overloaded by the user in order to print out the information stored at any of the derived classes."""
		...

	def setNodePointer(self, pqNode : PQNode[ T, X, Y ]) -> None:
		"""The functionsetNodePointer()sets the private memberm_nodePointer."""
		...

	def userStructInfo(self) -> X:
		"""Returns the information of any node."""
		...

	def userStructInternal(self) -> Y:
		"""Returns the information of any internal node."""
		...

	def userStructKey(self) -> T:
		"""Returns the key of a leaf."""
		...
