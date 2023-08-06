# file stubs/ogdf/fast_multipole_embedder/LinearQuadtree/bottom_up_traversal_functor.py generated from structogdf_1_1fast__multipole__embedder_1_1_linear_quadtree_1_1bottom__up__traversal__functor
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
F = TypeVar('F')

CondType = TypeVar('CondType')

class bottom_up_traversal_functor(Generic[F, CondType]):

	"""bottom up traversal of the subtree of a given node"""

	cond : CondType = ...

	func : F = ...

	tree : LinearQuadtree = ...

	@overload
	def __init__(self, t : LinearQuadtree, f : F) -> None:
		...

	@overload
	def __init__(self, t : LinearQuadtree, f : F, c : CondType) -> None:
		...

	def __call__(self, u : NodeID) -> None:
		...
