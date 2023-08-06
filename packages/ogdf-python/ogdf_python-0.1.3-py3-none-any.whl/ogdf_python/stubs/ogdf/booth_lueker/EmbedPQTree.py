# file stubs/ogdf/booth_lueker/EmbedPQTree.py generated from classogdf_1_1booth__lueker_1_1_embed_p_q_tree
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
class EmbedPQTree(ogdf.PQTree[ edge, IndInfo , bool ]):

	def __init__(self) -> None:
		...

	def __destruct__(self) -> None:
		...

	def clientDefinedEmptyNode(self, nodePtr : PQNode[edge,IndInfo, bool ]) -> None:
		"""If the user wishes to use different flags in a derived class ofPQTreethat are not available in this implementation, he can overload this function to make a valid cleanup of the nodes."""
		...

	def emptyAllPertinentNodes(self) -> None:
		"""Cleans up all flags that have been set in the pertinent nodes during the reduction process."""
		...

	def getFront(self, nodePtr : PQNode[edge,IndInfo, bool ], leafKeys : SListPure[PQBasicKey[edge,IndInfo, bool ]  ]) -> None:
		...

	@overload
	def Initialize(self, leafKeys : SListPure[PlanarLeafKey[IndInfo]  ]) -> int:
		...

	@overload
	def Initialize(self, leafKeys : SListPure[PQLeafKey[edge,IndInfo, bool ]  ]) -> int:
		...

	@overload
	def Reduction(self, leafKeys : SListPure[PlanarLeafKey[IndInfo]  ]) -> bool:
		...

	@overload
	def Reduction(self, leafKeys : SListPure[PQLeafKey[edge,IndInfo, bool ]  ]) -> bool:
		...

	def ReplaceRoot(self, leafKeys : SListPure[PlanarLeafKey[IndInfo]  ], frontier : SListPure[edge], opposed : SListPure[node], nonOpposed : SListPure[node], v : node) -> None:
		...

	def scanLeftEndmost(self, nodePtr : PQNode[edge,IndInfo, bool ]) -> PQNode[edge,IndInfo, bool ]:
		...

	def scanNextSib(self, nodePtr : PQNode[edge,IndInfo, bool ], other : PQNode[edge,IndInfo, bool ]) -> PQNode[edge,IndInfo, bool ]:
		...

	def scanRightEndmost(self, nodePtr : PQNode[edge,IndInfo, bool ]) -> PQNode[edge,IndInfo, bool ]:
		...

	def scanSibLeft(self, nodePtr : PQNode[edge,IndInfo, bool ]) -> PQNode[edge,IndInfo, bool ]:
		...

	def scanSibRight(self, nodePtr : PQNode[edge,IndInfo, bool ]) -> PQNode[edge,IndInfo, bool ]:
		...

	def clientLeftEndmost(self, nodePtr : PQNode[edge,IndInfo, bool ]) -> PQNode[edge,IndInfo, bool ]:
		...

	def clientNextSib(self, nodePtr : PQNode[edge,IndInfo, bool ], other : PQNode[edge,IndInfo, bool ]) -> PQNode[edge,IndInfo, bool ]:
		...

	def clientPrintStatus(self, nodePtr : PQNode[edge,IndInfo, bool ]) -> str:
		...

	def clientRightEndmost(self, nodePtr : PQNode[edge,IndInfo, bool ]) -> PQNode[edge,IndInfo, bool ]:
		...

	def clientSibLeft(self, nodePtr : PQNode[edge,IndInfo, bool ]) -> PQNode[edge,IndInfo, bool ]:
		...

	def clientSibRight(self, nodePtr : PQNode[edge,IndInfo, bool ]) -> PQNode[edge,IndInfo, bool ]:
		...

	@overload
	def front(self, nodePtr : PQNode[edge,IndInfo, bool ], leafKeys : SListPure[PQBasicKey[edge,IndInfo, bool ]  ]) -> None:
		...

	@overload
	def front(self, nodePtr : PQNode[edge,IndInfo, bool ], leafKeys : SListPure[PQLeafKey[edge,IndInfo, bool ]  ]) -> None:
		...
