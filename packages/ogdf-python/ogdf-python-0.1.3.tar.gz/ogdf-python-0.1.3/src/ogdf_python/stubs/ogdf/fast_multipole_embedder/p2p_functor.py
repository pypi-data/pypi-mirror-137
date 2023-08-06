# file stubs/ogdf/fast_multipole_embedder/p2p_functor.py generated from structogdf_1_1fast__multipole__embedder_1_1p2p__functor
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
class p2p_functor(object):

	"""Local-to-Point functor."""

	fx : float = ...

	fy : float = ...

	tree : LinearQuadtree = ...

	def __init__(self, t : LinearQuadtree, x : float, y : float) -> None:
		...

	@overload
	def __call__(self, nodeIndex : LinearQuadtree.NodeID) -> None:
		...

	@overload
	def __call__(self, nodeIndexA : LinearQuadtree.NodeID, nodeIndexB : LinearQuadtree.NodeID) -> None:
		...
