# file stubs/ogdf/PQNode.py generated from classogdf_1_1_p_q_node
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
Y = TypeVar('Y')

T = TypeVar('T')

X = TypeVar('X')

class PQNode(Generic[T, X, Y]):

	"""The class templatePQBasicKeyis an abstract base class."""

	#: Stores all full children of a node during a reduction.
	fullChildren : List[PQNode[ T, X, Y ]  ] = ...

	m_childCount : int = ...

	#: Needed for debuging purposes.
	m_debugTreeNumber : int = ...

	#: Stores a pointer to the first full child of a Q-node.
	m_firstFull : PQNode[ T, X, Y ] = ...

	#: Each node that has been introduced once into the tree gets a unique number.
	m_identificationNumber : int = ...

	m_leftEndmost : PQNode[ T, X, Y ] = ...

	#: Is a pointer to the parent.
	m_parent : PQNode[ T, X, Y ] = ...

	#: Stores the type of the parent which can be either a P- or Q-node.
	m_parentType : PQNodeType = ...

	#: Stores the number of pertinent children of the node.
	m_pertChildCount : int = ...

	#: Stores the number of pertinent leaves in the frontier of the node.
	m_pertLeafCount : int = ...

	#: Stores a pointer to the corresponding information of the node.
	m_pointerToInfo : PQNodeKey[ T, X, Y ] = ...

	#: Stores a pointer to one child, thereference childof the doubly linked cirkular list of children of a P-node.
	m_referenceChild : PQNode[ T, X, Y ] = ...

	#: Is a pointer to the parent, in case that the parent is a P-node and the node itself is its reference child.
	m_referenceParent : PQNode[ T, X, Y ] = ...

	#: Stores the right endmost child of a Q-node.
	m_rightEndmost : PQNode[ T, X, Y ] = ...

	#: Stores a pointer ot the left sibling ofPQNode.
	m_sibLeft : PQNode[ T, X, Y ] = ...

	#: Stores a pointer ot the right sibling ofPQNode.
	m_sibRight : PQNode[ T, X, Y ] = ...

	#: Stores all partial children of a node during a reduction.
	partialChildren : List[PQNode[ T, X, Y ]  ] = ...

	@overload
	def __init__(self, count : int) -> None:
		"""The (second) constructor is called, if no information is available or neccessary."""
		...

	@overload
	def __init__(self, count : int, infoPtr : PQNodeKey[ T, X, Y ]) -> None:
		"""The (first) constructor combines the node with its information and will automatically set thePQBasicKey::m_nodePointer(see basicKey) of the element of typePQNodeKey."""
		...

	def __destruct__(self) -> None:
		"""The destructor does not delete any accompanying information class asPQLeafKey,PQNodeKeyandPQInternalKey."""
		...

	def changeEndmost(self, oldEnd : PQNode[ T, X, Y ], newEnd : PQNode[ T, X, Y ]) -> bool:
		"""The functionchangeEndmost()replaces the old endmost childoldEndof the node by a new childnewEnd."""
		...

	def changeSiblings(self, oldSib : PQNode[ T, X, Y ], newSib : PQNode[ T, X, Y ]) -> bool:
		"""The functionchangeSiblings()replaces the old siblingoldSibof the node by a new siblingnewSib."""
		...

	@overload
	def childCount(self) -> int:
		"""Returns the number of children of a node."""
		...

	@overload
	def childCount(self, count : int) -> None:
		"""Sets the number of children of a node."""
		...

	def endmostChild(self) -> bool:
		"""The functionendmostChild()checks if a node is endmost child of a Q-node."""
		...

	@overload
	def getEndmost(self, other : PQNode[ T, X, Y ]) -> PQNode[ T, X, Y ]:
		"""Returns one of the endmost children of node, if node is a Q-node."""
		...

	@overload
	def getEndmost(self, side : SibDirection) -> PQNode[ T, X, Y ]:
		"""Returns one of the endmost children of node, if node is a Q-node."""
		...

	def getInternal(self) -> PQInternalKey[ T, X, Y ]:
		"""getInternal()returns a pointer to thePQInternalKeyinformation of a node, in case that the node is supposed to havePQInternalKeyinformation, such as elements of the derived class templatePQInternalNode."""
		...

	def getKey(self) -> PQLeafKey[ T, X, Y ]:
		"""getKey()returns a pointer to the PQLeafKeyof a node, in case that the node is supposed to have a key, such as elements of the derived class templatePQLeaf."""
		...

	def getNextSib(self, other : PQNode[ T, X, Y ]) -> PQNode[ T, X, Y ]:
		"""The functiongetNextSib()returns one of the siblings of the node."""
		...

	def getNodeInfo(self) -> PQNodeKey[ T, X, Y ]:
		"""Returns the identification number of a node."""
		...

	def getSib(self, side : SibDirection) -> PQNode[ T, X, Y ]:
		"""The functiongetSib()returns one of the siblings of the node."""
		...

	def identificationNumber(self) -> int:
		"""Returns the identification number of a node."""
		...

	@overload
	def mark(self) -> PQNodeMark:
		"""mark()returns the variablePQLeaf::m_markin the derived classPQLeafandPQInternalNode."""
		...

	@overload
	def mark(self, _ : PQNodeMark) -> None:
		"""mark()sets the variablePQLeaf::m_markin the derived classPQLeafandPQInternalNode."""
		...

	@overload
	def parent(self) -> PQNode[ T, X, Y ]:
		"""The functionparent()returns a pointer to the parent of a node."""
		...

	@overload
	def parent(self, newParent : PQNode[ T, X, Y ]) -> PQNode[ T, X, Y ]:
		"""Sets the parent pointer of a node."""
		...

	@overload
	def parentType(self) -> PQNodeType:
		"""Returns the type of the parent of a node."""
		...

	@overload
	def parentType(self, newParentType : PQNodeType) -> None:
		"""Sets the type of the parent of a node."""
		...

	@overload
	def pertChildCount(self) -> int:
		"""Returs the number of pertinent children of a node."""
		...

	@overload
	def pertChildCount(self, count : int) -> None:
		"""Sets the number of pertinent children of a node."""
		...

	@overload
	def putSibling(self, newSib : PQNode[ T, X, Y ]) -> SibDirection:
		"""The default functionputSibling()stores a new sibling at a free sibling pointer of the node."""
		...

	@overload
	def putSibling(self, newSib : PQNode[ T, X, Y ], preference : SibDirection) -> SibDirection:
		"""The functionputSibling()with preference stores a new sibling at a free sibling pointer of the node."""
		...

	def referenceChild(self) -> PQNode[ T, X, Y ]:
		"""Returns a pointer to the reference child if node is a P-node."""
		...

	def referenceParent(self) -> PQNode[ T, X, Y ]:
		"""Returns the pointer to the parent if node is a reference child."""
		...

	def setInternal(self, pointerToInternal : PQInternalKey[ T, X, Y ]) -> bool:
		...

	def setKey(self, pointerToKey : PQLeafKey[ T, X, Y ]) -> bool:
		"""Sets a specified pointer variable in a derived class to the specified adress ofpointerToKeythat is of typePQLeafKey."""
		...

	def setNodeInfo(self, pointerToInfo : PQNodeKey[ T, X, Y ]) -> bool:
		"""Sets the pointerm_pointerToInfoto the specified adress ofpointerToInfo."""
		...

	@overload
	def status(self) -> PQNodeStatus:
		"""Returns the variablePQLeaf::m_statusin the derived classPQLeafandPQInternalNode."""
		...

	@overload
	def status(self, _ : PQNodeStatus) -> None:
		"""Sets the variablePQLeaf::m_statusin the derived classPQLeafandPQInternalNode."""
		...

	@overload
	def type(self) -> PQNodeType:
		"""Returns the variablePQInternalNode::m_typein the derived classPQLeafandPQInternalNode."""
		...

	@overload
	def type(self, _ : PQNodeType) -> None:
		"""Sets the variablePQInternalNode::m_typein the derived classPQLeafandPQInternalNode."""
		...
