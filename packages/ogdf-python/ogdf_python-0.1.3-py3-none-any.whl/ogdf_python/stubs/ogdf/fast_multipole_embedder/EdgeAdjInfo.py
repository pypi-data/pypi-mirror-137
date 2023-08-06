# file stubs/ogdf/fast_multipole_embedder/EdgeAdjInfo.py generated from classogdf_1_1fast__multipole__embedder_1_1_edge_adj_info
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
class EdgeAdjInfo(object):

	"""Information about an edge (16 bytes)."""

	#: First node of the pair.
	a : int = ...

	#: Next pair in the chain of the first node.
	a_next : int = ...

	#: Second node of the pair.
	b : int = ...

	#: Next pair in the chain of the second node.
	b_next : int = ...

	def nextEdgeAdjIndex(self, index : int) -> int:
		"""Returns the index of the next pair ofindex."""
		...

	def twinNode(self, index : int) -> int:
		"""Returns the other node (notindex)."""
		...
