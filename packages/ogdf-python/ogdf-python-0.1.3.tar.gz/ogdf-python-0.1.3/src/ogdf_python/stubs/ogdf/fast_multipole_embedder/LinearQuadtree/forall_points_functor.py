# file stubs/ogdf/fast_multipole_embedder/LinearQuadtree/forall_points_functor.py generated from structogdf_1_1fast__multipole__embedder_1_1_linear_quadtree_1_1forall__points__functor
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
Func = TypeVar('Func')

class forall_points_functor(Generic[Func]):

	"""simple functor for iterating over all points of a node"""

	func : Func = ...

	tree : LinearQuadtree = ...

	def __init__(self, t : LinearQuadtree, f : Func) -> None:
		...

	def __call__(self, u : NodeID) -> None:
		...
