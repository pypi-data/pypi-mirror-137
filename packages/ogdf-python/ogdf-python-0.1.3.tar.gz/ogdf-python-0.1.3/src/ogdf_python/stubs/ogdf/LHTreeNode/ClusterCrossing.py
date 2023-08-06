# file stubs/ogdf/LHTreeNode/ClusterCrossing.py generated from structogdf_1_1_l_h_tree_node_1_1_cluster_crossing
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
class ClusterCrossing(object):

	m_cNode : LHTreeNode = ...

	m_edge : edge = ...

	m_u : node = ...

	m_uc : node = ...

	m_uNode : LHTreeNode = ...

	@overload
	def __init__(self) -> None:
		...

	@overload
	def __init__(self, uc : node, cNode : LHTreeNode, u : node, uNode : LHTreeNode, e : edge) -> None:
		...
