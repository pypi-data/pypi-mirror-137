# file stubs/ogdf/fast_multipole_embedder/m2m_functor.py generated from structogdf_1_1fast__multipole__embedder_1_1m2m__functor
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
class m2m_functor(object):

	"""Multipole-to-Multipole functor."""

	expansions : LinearQuadtreeExpansion = ...

	tree : LinearQuadtree = ...

	def __init__(self, t : LinearQuadtree, e : LinearQuadtreeExpansion) -> None:
		...

	@overload
	def __call__(self, nodeIndex : LinearQuadtree.NodeID) -> None:
		...

	@overload
	def __call__(self, parent : LinearQuadtree.NodeID, child : LinearQuadtree.NodeID) -> None:
		...
