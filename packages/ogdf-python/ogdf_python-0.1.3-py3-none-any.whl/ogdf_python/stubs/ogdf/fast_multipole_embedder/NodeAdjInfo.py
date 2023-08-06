# file stubs/ogdf/fast_multipole_embedder/NodeAdjInfo.py generated from classogdf_1_1fast__multipole__embedder_1_1_node_adj_info
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
class NodeAdjInfo(object):

	"""Information about incident edges (16 bytes)."""

	#: Total count of pairs where is either the first or second node.
	degree : int = ...

	#: The first pair in the edges chain.
	firstEntry : int = ...

	#: The last pair in the edges chain.
	lastEntry : int = ...

	#: Not used yet.
	unused : int = ...
