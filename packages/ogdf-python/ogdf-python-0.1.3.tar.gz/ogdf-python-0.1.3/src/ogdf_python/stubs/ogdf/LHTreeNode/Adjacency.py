# file stubs/ogdf/LHTreeNode/Adjacency.py generated from structogdf_1_1_l_h_tree_node_1_1_adjacency
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
class Adjacency(object):

	m_u : node = ...

	m_v : LHTreeNode = ...

	m_weight : int = ...

	@overload
	def __init__(self) -> None:
		...

	@overload
	def __init__(self, u : node, vNode : LHTreeNode, weight : int = 1) -> None:
		...
