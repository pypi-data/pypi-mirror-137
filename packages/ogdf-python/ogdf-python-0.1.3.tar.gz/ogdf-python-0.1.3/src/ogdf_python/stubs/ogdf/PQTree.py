# file stubs/ogdf/PQTree.py generated from classogdf_1_1_p_q_tree
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
Y = TypeVar('Y')

T = TypeVar('T')

X = TypeVar('X')

class PQTree(Generic[T, X, Y]):

	@overload
	def writeGML(self, fileName : str) -> None:
		"""The functionwriteGML()prints the PQ-tree in the GML fileformat."""
		...

	@overload
	def writeGML(self, os : std.ostream) -> None:
		...

	#: Stores the total number of nodes that have been allocated.
	m_identificationNumber : int = ...

	#: Stores the number of leaves.
	m_numberOfLeaves : int = ...

	#: Stores all nodes that have been markedPQNodeRoot::PQNodeStatus::FullorPQNodeRoot::PQNodeStatus::Partialduring a reduction.
	m_pertinentNodes : List[PQNode[ T, X, Y ]  ] = ...

	#: a pointer to the root of the pertinent subtree.
	m_pertinentRoot : PQNode[ T, X, Y ] = ...

	#: a pointer to the virtual root of the pertinent subtree, in case that the pertinent root cannot be detected.
	m_pseudoRoot : PQNode[ T, X, Y ] = ...

	#: a pointer to the root of the $PQ$-tree.
	m_root : PQNode[ T, X, Y ] = ...

	def __init__(self) -> None:
		...

	def __destruct__(self) -> None:
		"""Destructor."""
		...

	def addNewLeavesToTree(self, father : PQInternalNode[ T, X,
	                        Y ], leafKeys : SListPure[PQLeafKey[ T, X, Y ] 
	                        ]) -> bool:
		"""Adds a set of elements to the already existing set of elements of a PQ-tree."""
		...

	def CleanNode(self, _ : PQNode[ T, X, Y ]) -> None:
		...

	def Cleanup(self) -> None:
		"""Removes the entire PQ-tree."""
		...

	def clientDefinedEmptyNode(self, nodePtr : PQNode[ T, X, Y ]) -> None:
		"""If the user wishes to use different flags in a derived class ofPQTreethat are not available in this implementation, he can overload this function to make a valid cleanup of the nodes."""
		...

	def emptyAllPertinentNodes(self) -> None:
		"""Cleans up all flags that have been set in the pertinent nodes during the reduction process."""
		...

	def emptyNode(self, nodePtr : PQNode[ T, X, Y ]) -> None:
		"""Cleans up all stacks, flags and pointers of a pertinent node that has been visited during the reduction process."""
		...

	def front(self, nodePtr : PQNode[ T, X, Y ], leafKeys : SListPure[PQLeafKey[ T, X, Y ] 
	                        ]) -> None:
		"""Returns the keys stored in the leaves of the front ofnodePtr."""
		...

	def Initialize(self, leafKeys : SListPure[PQLeafKey[ T, X, Y ] 
	                        ]) -> int:
		"""Initializes the PQ-tree with a set of elements."""
		...

	def Reduction(self, leafKeys : SListPure[PQLeafKey[ T, X, Y ] 
	                        ]) -> bool:
		"""Tests whether permissible permutations of the elements of U exist such that the elements of a subset S of U, stored inleafKeys, form a consecutive sequence."""
		...

	def root(self) -> PQNode[ T, X, Y ]:
		"""Returns a pointer of the root node of thePQTree."""
		...

	@overload
	def addNodeToNewParent(self, parent : PQNode[ T, X, Y ], child : PQNode[ T, X, Y ]) -> bool:
		"""Adds a nodechildas a child to another node specified inparent."""
		...

	@overload
	def addNodeToNewParent(self, parent : PQNode[ T, X, Y ], child : PQNode[ T, X, Y ], leftBrother : PQNode[ T, X, Y ], rightBrother : PQNode[ T, X, Y ]) -> bool:
		"""Adds a nodechildto the children of another node specified inparent."""
		...

	def Bubble(self, leafKeys : SListPure[PQLeafKey[ T, X, Y ] 
	                        ]) -> bool:
		"""Realizes a function described in [Booth]."""
		...

	def checkIfOnlyChild(self, child : PQNode[ T, X, Y ], parent : PQNode[ T, X, Y ]) -> bool:
		"""Checks ifchildis the only child ofparent."""
		...

	def clientLeftEndmost(self, nodePtr : PQNode[ T, X, Y ]) -> PQNode[ T, X, Y ]:
		...

	def clientNextSib(self, nodePtr : PQNode[ T, X, Y ], other : PQNode[ T, X, Y ]) -> PQNode[ T, X, Y ]:
		...

	def clientPrintNodeCategorie(self, nodePtr : PQNode[ T, X, Y ]) -> int:
		"""If the user wishes to use different flags in a derived class ofPQTreethat are not available in this implementation, he can overload this function."""
		...

	def clientPrintStatus(self, nodePtr : PQNode[ T, X, Y ]) -> str:
		"""If the user wishes to use different status in a derived class ofPQTreethat are not available in this implementation, he can overload this function."""
		...

	def clientPrintType(self, nodePtr : PQNode[ T, X, Y ]) -> str:
		"""If the user wishes to use different types in a derived class ofPQTreethat are not available in this implementation, he can overload this function."""
		...

	def clientRightEndmost(self, nodePtr : PQNode[ T, X, Y ]) -> PQNode[ T, X, Y ]:
		...

	def clientSibLeft(self, nodePtr : PQNode[ T, X, Y ]) -> PQNode[ T, X, Y ]:
		...

	def clientSibRight(self, nodePtr : PQNode[ T, X, Y ]) -> PQNode[ T, X, Y ]:
		...

	def destroyNode(self, nodePtr : PQNode[ T, X, Y ]) -> None:
		"""Marks a node asPQNodeRoot::PQNodeStatus::ToBeDeleted."""
		...

	def exchangeNodes(self, oldNode : PQNode[ T, X, Y ], newNode : PQNode[ T, X, Y ]) -> None:
		"""Replaces theoldNodeby thenewNodein the tree."""
		...

	def fullChildren(self, nodePtr : PQNode[ T, X, Y ]) -> List[PQNode[ T, X, Y ]  ]:
		...

	def linkChildrenOfQnode(self, installed : PQNode[ T, X, Y ], newChild : PQNode[ T, X, Y ]) -> None:
		"""Links the two endmost children of twodifferentQ-nodes via their sibling pointers together."""
		...

	def partialChildren(self, nodePtr : PQNode[ T, X, Y ]) -> List[PQNode[ T, X, Y ]  ]:
		...

	def Reduce(self, leafKeys : SListPure[PQLeafKey[ T, X, Y ] 
	                        ]) -> bool:
		"""Performs the reduction of the pertinent leaves with the help of the template matchings, designed by Booth and Lueker."""
		...

	def removeChildFromSiblings(self, nodePtr : PQNode[ T, X, Y ]) -> None:
		"""Removes the nodenodePtrfrom the doubly linked list of its parent."""
		...

	def removeNodeFromTree(self, parent : PQNode[ T, X, Y ], child : PQNode[ T, X, Y ]) -> int:
		"""The objective is to remove a nodechildfrom the PQ-tree."""
		...

	def templateL1(self, nodePtr : PQNode[ T, X, Y ], isRoot : bool) -> bool:
		"""Template matching for leaves."""
		...

	def templateP1(self, nodePtr : PQNode[ T, X, Y ], isRoot : bool) -> bool:
		"""Template matching for P-nodes with only full children."""
		...

	def templateP2(self, nodePtr : PQNode[ T, X, Y ]) -> bool:
		"""Template matching for a P-node with fullandempty children that is the root of the pertinent subtree."""
		...

	def templateP3(self, nodePtr : PQNode[ T, X, Y ]) -> bool:
		"""Template matching for a P-node with fullandempty children that isnotthe root of the pertinent subtree."""
		...

	def templateP4(self, nodePtr : PQNode[ T, X, Y ]) -> bool:
		"""Template matching for a P-node with full, empty and exactly one partial children."""
		...

	def templateP5(self, nodePtr : PQNode[ T, X, Y ]) -> bool:
		"""Template matching for a P-node with full, empty children and exactly one partial child."""
		...

	def templateP6(self, nodePtr : PQNode[ T, X, Y ]) -> bool:
		"""Template matching for a P-node with full, empty and exactly two partial children."""
		...

	def templateQ1(self, nodePtr : PQNode[ T, X, Y ], isRoot : bool) -> bool:
		"""Template matching for Q-nodes with only full children."""
		...

	def templateQ2(self, nodePtr : PQNode[ T, X, Y ], isRoot : bool) -> bool:
		"""Template matching for Q-nodes with a pertinent sequence of children on one side of the Q-node."""
		...

	def templateQ3(self, nodePtr : PQNode[ T, X, Y ]) -> bool:
		...
