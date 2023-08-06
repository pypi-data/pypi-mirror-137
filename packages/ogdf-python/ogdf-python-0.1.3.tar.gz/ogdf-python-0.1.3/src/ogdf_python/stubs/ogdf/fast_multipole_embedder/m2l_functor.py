# file stubs/ogdf/fast_multipole_embedder/m2l_functor.py generated from structogdf_1_1fast__multipole__embedder_1_1m2l__functor
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
class m2l_functor(object):

	"""Multipole-to-Local functor."""

	expansions : LinearQuadtreeExpansion = ...

	def __init__(self, e : LinearQuadtreeExpansion) -> None:
		...

	def __call__(self, nodeIndexSource : LinearQuadtree.NodeID, nodeIndexReceiver : LinearQuadtree.NodeID) -> None:
		...
