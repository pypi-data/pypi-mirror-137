# file stubs/ogdf/booth_lueker/EmbedIndicator.py generated from classogdf_1_1booth__lueker_1_1_embed_indicator
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
class EmbedIndicator(ogdf.PQNode[ edge, IndInfo , bool ]):

	def __init__(self, count : int, infoPtr : PQNodeKey[edge,IndInfo, bool ]) -> None:
		...

	def __destruct__(self) -> None:
		...

	def getInternal(self) -> PQInternalKey[edge,IndInfo, bool ]:
		...

	def getKey(self) -> PQLeafKey[edge,IndInfo, bool ]:
		...

	@overload
	def mark(self) -> PQNodeMark:
		...

	@overload
	def mark(self, _ : PQNodeMark) -> None:
		"""mark()sets the variablePQLeaf::m_markin the derived classPQLeafandPQInternalNode."""
		...

	def setInternal(self, pointerToInternal : PQInternalKey[edge,IndInfo, bool ]) -> bool:
		...

	def setKey(self, pointerToKey : PQLeafKey[edge,IndInfo, bool ]) -> bool:
		"""Sets a specified pointer variable in a derived class to the specified adress ofpointerToKeythat is of typePQLeafKey."""
		...

	@overload
	def status(self) -> PQNodeStatus:
		...

	@overload
	def status(self, _ : PQNodeStatus) -> None:
		"""Sets the variablePQLeaf::m_statusin the derived classPQLeafandPQInternalNode."""
		...

	@overload
	def type(self) -> PQNodeType:
		...

	@overload
	def type(self, _ : PQNodeType) -> None:
		"""Sets the variablePQInternalNode::m_typein the derived classPQLeafandPQInternalNode."""
		...
