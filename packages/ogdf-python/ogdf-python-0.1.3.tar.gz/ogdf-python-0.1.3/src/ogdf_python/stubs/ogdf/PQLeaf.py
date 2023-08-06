# file stubs/ogdf/PQLeaf.py generated from classogdf_1_1_p_q_leaf
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
Y = TypeVar('Y')

T = TypeVar('T')

X = TypeVar('X')

class PQLeaf(ogdf.PQNode[ T, X, Y ], Generic[T, X, Y]):

	"""The datastructure PQ-tree was designed to present a set of permutations on an arbitrary set of elements."""

	@overload
	def __init__(self, count : int, stat : PQNodeRoot.PQNodeStatus, keyPtr : PQLeafKey[ T, X, Y ]) -> None:
		...

	@overload
	def __init__(self, count : int, stat : PQNodeRoot.PQNodeStatus, keyPtr : PQLeafKey[ T, X, Y ], infoPtr : PQNodeKey[ T, X, Y ]) -> None:
		"""The client may choose between two different constructors."""
		...

	def __destruct__(self) -> None:
		"""The destructor does not delete any accompanying information class asPQLeafKey,PQNodeKeyandPQInternalKey."""
		...

	def getInternal(self) -> PQInternalKey[ T, X, Y ]:
		"""getInternal()returns 0."""
		...

	def getKey(self) -> PQLeafKey[ T, X, Y ]:
		"""getKey()returns a pointer to thePQLeafKeyofPQLeaf."""
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
		"""setInternal()accepts only pointerspointerToInternal= 0."""
		...

	def setKey(self, pointerToKey : PQLeafKey[ T, X, Y ]) -> bool:
		"""setKey()sets the pointer variablem_pointerToKeyto the specified address ofpointerToKeythat is of typePQLeafKey."""
		...

	@overload
	def status(self) -> PQNodeRoot.PQNodeStatus:
		"""Returns the variablem_statusin the derived classPQLeaf."""
		...

	@overload
	def status(self, s : PQNodeRoot.PQNodeStatus) -> None:
		"""Sets the variablem_statusin the derived classPQLeaf."""
		...

	@overload
	def type(self) -> PQNodeRoot.PQNodeType:
		"""Returns the variablePQInternalNode::m_typein the derived classPQLeaf."""
		...

	@overload
	def type(self, _ : PQNodeRoot.PQNodeType) -> None:
		"""Sets the variablePQInternalNode::m_typein the derived classPQLeaf."""
		...
