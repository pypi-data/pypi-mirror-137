# file stubs/ogdf/fast_multipole_embedder/l2p_functor.py generated from structogdf_1_1fast__multipole__embedder_1_1l2p__functor
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
class l2p_functor(object):

	"""Local-to-Point functor."""

	expansions : LinearQuadtreeExpansion = ...

	fx : float = ...

	fy : float = ...

	tree : LinearQuadtree = ...

	def __init__(self, t : LinearQuadtree, e : LinearQuadtreeExpansion, x : float, y : float) -> None:
		...

	@overload
	def __call__(self, nodeIndex : LinearQuadtree.NodeID, pointIndex : LinearQuadtree.PointID) -> None:
		...

	@overload
	def __call__(self, pointIndex : LinearQuadtree.PointID) -> None:
		...
