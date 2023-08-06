# file stubs/ogdf/energybased/dtree/DTree/Node.py generated from structogdf_1_1energybased_1_1dtree_1_1_d_tree_1_1_node
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
class Node(object):

	"""The node class."""

	#: index of the children
	child : int = ...

	#: the first point in the sorted order covered by this subtree
	firstPoint : int = ...

	#: the level of the node in a complete quadtree
	level : int = ...

	#: the next node on the same layer (leaf or inner node layer)
	next : int = ...

	#: number of children
	numChilds : int = ...

	#: the number of points covered by this subtree
	numPoints : int = ...
