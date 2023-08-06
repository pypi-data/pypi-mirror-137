# file stubs/ogdf/fast_multipole_embedder/p2m_functor.py generated from structogdf_1_1fast__multipole__embedder_1_1p2m__functor
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
class p2m_functor(object):

	"""Point-to-Multipole functor."""

	expansions : LinearQuadtreeExpansion = ...

	tree : LinearQuadtree = ...

	def __init__(self, t : LinearQuadtree, e : LinearQuadtreeExpansion) -> None:
		...

	def __call__(self, nodeIndex : LinearQuadtree.NodeID) -> None:
		...
