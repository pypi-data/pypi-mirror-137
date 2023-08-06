# file stubs/ogdf/fast_multipole_embedder/LinearQuadtree/is_leaf_condition_functor.py generated from structogdf_1_1fast__multipole__embedder_1_1_linear_quadtree_1_1is__leaf__condition__functor
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
class is_leaf_condition_functor(object):

	tree : LinearQuadtree = ...

	def __init__(self, t : LinearQuadtree) -> None:
		...

	def __call__(self, u : NodeID) -> bool:
		...
