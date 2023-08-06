# file stubs/ogdf/fast_multipole_embedder/LinearQuadtree/forall_tree_nodes_functor.py generated from structogdf_1_1fast__multipole__embedder_1_1_linear_quadtree_1_1forall__tree__nodes__functor
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
F = TypeVar('F')

class forall_tree_nodes_functor(Generic[F]):

	"""simple functor for iterating over all nodes"""

	begin : NodeID = ...

	func : F = ...

	numNodes : int = ...

	tree : LinearQuadtree = ...

	def __init__(self, t : LinearQuadtree, f : F, b : NodeID, num : int) -> None:
		...

	def __call__(self) -> None:
		...
