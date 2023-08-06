# file stubs/ogdf/fast_multipole_embedder/LinearQuadtree/forall_ordered_pairs_of_children_functor.py generated from structogdf_1_1fast__multipole__embedder_1_1_linear_quadtree_1_1forall__ordered__pairs__of__children__functor
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
F = TypeVar('F')

class forall_ordered_pairs_of_children_functor(Generic[F]):

	"""functor for iterating over all ordered pairs of children of a node"""

	func : F = ...

	tree : LinearQuadtree = ...

	def __init__(self, t : LinearQuadtree, f : F) -> None:
		...

	def __call__(self, u : NodeID) -> None:
		...
