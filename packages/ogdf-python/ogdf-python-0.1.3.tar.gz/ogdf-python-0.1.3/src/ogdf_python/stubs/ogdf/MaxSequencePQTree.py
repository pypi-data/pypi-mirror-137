# file stubs/ogdf/MaxSequencePQTree.py generated from classogdf_1_1_max_sequence_p_q_tree
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
T = TypeVar('T')

Y = TypeVar('Y')

class MaxSequencePQTree(ogdf.PQTree[ T, whaInfo , Y ], Generic[T, Y]):

	"""The class templateMaxSequencePQTreeis designed to compute a maximal consecutive sequence of pertinent leaves in a PQ-tree."""

	#: Used to store all pertinent Nodes of the pertinent subtree before removing the minimal pertinent subsequence.
	cleanUp : SListPure[PQNode[ T,whaInfo, Y ]  ] = ...

	#: Used to store all eliminated nodes (status==PQNodeRoot::PQNodeStatus::Eliminated) of thePQTree.
	eliminatedNodes : SListPure[PQNode[ T,whaInfo, Y ]  ] = ...

	def __init__(self) -> None:
		...

	def __destruct__(self) -> None:
		...

	def CleanNode(self, nodePtr : PQNode[ T,whaInfo, Y ]) -> None:
		"""Frees the memory allocated for the node information class of a node in thePQTree."""
		...

	def clientDefinedEmptyNode(self, nodePtr : PQNode[ T,whaInfo, Y ]) -> None:
		"""Does a clean up of a node. Called byemptyAllPertinentNodes."""
		...

	def determineMinRemoveSequence(self, leafKeys : SListPure[PQLeafKey[ T,whaInfo, Y ]  ], eliminatedKeys : SList[PQLeafKey[ T,whaInfo, Y ]  ]) -> int:
		"""Computes the maximal pertinent sequenceS'of elements of the setS, that can be reduced in a PQ-tree."""
		...

	def emptyAllPertinentNodes(self) -> None:
		"""Does a clean up after a reduction."""
		...

	def Bubble(self, leafKeys : SListPure[PQLeafKey[ T,whaInfo, Y ]  ]) -> bool:
		"""The functionBubble()is an overloaded function of the base template classPQTree."""
		...

	def GetParent(self, nodePtr : PQNode[ T,whaInfo, Y ]) -> PQNode[ T,whaInfo, Y ]:
		"""Computes for the nodenodePtrits valid parent in the PQ-tree."""
		...
