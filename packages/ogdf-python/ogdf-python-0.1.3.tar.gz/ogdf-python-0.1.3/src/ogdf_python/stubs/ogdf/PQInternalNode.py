# file stubs/ogdf/PQInternalNode.py generated from classogdf_1_1_p_q_internal_node
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
Y = TypeVar('Y')

T = TypeVar('T')

X = TypeVar('X')

class PQInternalNode(ogdf.PQNode[ T, X, Y ], Generic[T, X, Y]):

	"""The class templatePQInternalNodeis used to present P-nodes and Q-nodes in the PQ-Tree."""

	@overload
	def __init__(self, count : int, typ : PQNodeRoot.PQNodeType, stat : PQNodeRoot.PQNodeStatus) -> None:
		...

	@overload
	def __init__(self, count : int, typ : PQNodeRoot.PQNodeType, stat : PQNodeRoot.PQNodeStatus, internalPtr : PQInternalKey[ T, X, Y ]) -> None:
		...

	@overload
	def __init__(self, count : int, typ : PQNodeRoot.PQNodeType, stat : PQNodeRoot.PQNodeStatus, internalPtr : PQInternalKey[ T, X, Y ], infoPtr : PQNodeKey[ T, X, Y ]) -> None:
		...

	@overload
	def __init__(self, count : int, typ : PQNodeRoot.PQNodeType, stat : PQNodeRoot.PQNodeStatus, infoPtr : PQNodeKey[ T, X, Y ]) -> None:
		...

	def __destruct__(self) -> None:
		"""The destructor does not delete any accompanying information class asPQLeafKey,PQNodeKeyandPQInternalKey."""
		...

	def getInternal(self) -> PQInternalKey[ T, X, Y ]:
		"""Returns a pointer to thePQInternalKeyinformation."""
		...

	def getKey(self) -> PQLeafKey[ T, X, Y ]:
		"""Returns 0. An element of typePQInternalNodedoes not have aPQLeafKey."""
		...

	@overload
	def mark(self) -> PQNodeRoot.PQNodeMark:
		"""Returns the variablem_mark."""
		...

	@overload
	def mark(self, m : PQNodeRoot.PQNodeMark) -> None:
		"""Sets the variablem_mark."""
		...

	def setInternal(self, pointerToInternal : PQInternalKey[ T, X, Y ]) -> bool:
		"""setInternal()sets the pointer variablem_pointerToInternalto the specified adress ofpointerToInternalthat is of typePQInternalKey."""
		...

	def setKey(self, pointerToKey : PQLeafKey[ T, X, Y ]) -> bool:
		"""Accepts only pointerspointerToKey= 0."""
		...

	@overload
	def status(self) -> PQNodeRoot.PQNodeStatus:
		"""Returns the variablem_statusin the derived classPQInternalNode."""
		...

	@overload
	def status(self, s : PQNodeRoot.PQNodeStatus) -> None:
		"""Sets the variablem_statusin the derived classPQInternalNode."""
		...

	@overload
	def type(self) -> PQNodeRoot.PQNodeType:
		"""Returns the variablem_typein the derived classPQInternalNode."""
		...

	@overload
	def type(self, t : PQNodeRoot.PQNodeType) -> None:
		"""Sets the variablem_typein the derived classPQInternalNode."""
		...
