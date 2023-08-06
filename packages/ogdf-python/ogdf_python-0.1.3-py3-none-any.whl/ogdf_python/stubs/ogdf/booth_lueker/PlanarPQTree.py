# file stubs/ogdf/booth_lueker/PlanarPQTree.py generated from classogdf_1_1booth__lueker_1_1_planar_p_q_tree
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
class PlanarPQTree(ogdf.PQTree[ edge, IndInfo , bool ]):

	def __init__(self) -> None:
		...

	def __destruct__(self) -> None:
		...

	def emptyAllPertinentNodes(self) -> None:
		"""Does a clean up after a reduction."""
		...

	@overload
	def Initialize(self, leafKeys : SListPure[PlanarLeafKey[IndInfo]  ]) -> int:
		"""Initializes a new PQ-tree with a set of leaves."""
		...

	@overload
	def Initialize(self, leafKeys : SListPure[PQLeafKey[edge,IndInfo, bool ]  ]) -> int:
		...

	@overload
	def Reduction(self, leafKeys : SListPure[PlanarLeafKey[IndInfo]  ]) -> bool:
		"""Reduces a set of leaves."""
		...

	@overload
	def Reduction(self, leafKeys : SListPure[PQLeafKey[edge,IndInfo, bool ]  ]) -> bool:
		...

	def ReplaceRoot(self, leafKeys : SListPure[PlanarLeafKey[IndInfo]  ]) -> None:
		"""Replaces the pertinent subtree by a set of new leaves."""
		...
