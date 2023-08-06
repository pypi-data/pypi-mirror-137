# file stubs/ogdf/PlanarSubgraphPQTree.py generated from classogdf_1_1_planar_subgraph_p_q_tree
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
class PlanarSubgraphPQTree(ogdf.MaxSequencePQTree[ edge, bool ]):

	PlanarLeafKey : Type = booth_lueker.PlanarLeafKey[whaInfo]

	def __init__(self) -> None:
		...

	def __destruct__(self) -> None:
		...

	@overload
	def Initialize(self, leafKeys : SListPure[PlanarLeafKey]) -> int:
		"""Initializes a new PQ-tree with a set of leaves."""
		...

	@overload
	def Initialize(self, leafKeys : SListPure[PQLeafKey[edge,whaInfo, bool ]  ]) -> int:
		...

	@overload
	def Reduction(self, leafKeys : SListPure[PlanarLeafKey], eliminatedKeys : SList[PQLeafKey[edge,whaInfo, bool ]  ]) -> bool:
		"""Reduces a set of leaves."""
		...

	@overload
	def Reduction(self, leafKeys : SListPure[PQLeafKey[edge,whaInfo, bool ]  ]) -> bool:
		...

	def ReplaceRoot(self, leafKeys : SListPure[PlanarLeafKey]) -> None:
		"""Replaces the pertinent subtree by a set of new leaves."""
		...
