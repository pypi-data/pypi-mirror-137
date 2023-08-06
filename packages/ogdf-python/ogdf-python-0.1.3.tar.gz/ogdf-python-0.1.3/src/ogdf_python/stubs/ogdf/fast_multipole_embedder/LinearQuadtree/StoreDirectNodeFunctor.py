# file stubs/ogdf/fast_multipole_embedder/LinearQuadtree/StoreDirectNodeFunctor.py generated from structogdf_1_1fast__multipole__embedder_1_1_linear_quadtree_1_1_store_direct_node_functor
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
class StoreDirectNodeFunctor(object):

	tree : LinearQuadtree = ...

	def __init__(self, t : LinearQuadtree) -> None:
		...

	def __call__(self, a : NodeID) -> None:
		...
