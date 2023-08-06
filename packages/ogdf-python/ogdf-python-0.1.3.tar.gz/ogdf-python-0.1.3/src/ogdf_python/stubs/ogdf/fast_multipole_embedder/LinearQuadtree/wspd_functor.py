# file stubs/ogdf/fast_multipole_embedder/LinearQuadtree/wspd_functor.py generated from structogdf_1_1fast__multipole__embedder_1_1_linear_quadtree_1_1wspd__functor
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
DPairFuncType = TypeVar('DPairFuncType')

DNodeFuncType = TypeVar('DNodeFuncType')

BranchCondType = TypeVar('BranchCondType')

WSPairFuncType = TypeVar('WSPairFuncType')

class wspd_functor(Generic[WSPairFuncType, DPairFuncType, DNodeFuncType, BranchCondType]):

	BranchCondFunction : BranchCondType = ...

	DNodeFunction : DNodeFuncType = ...

	DPairFunction : DPairFuncType = ...

	tree : LinearQuadtree = ...

	WSFunction : WSPairFuncType = ...

	@overload
	def __init__(self, t : LinearQuadtree, wsf : WSPairFuncType, dpf : DPairFuncType, dnf : DNodeFuncType) -> None:
		...

	@overload
	def __init__(self, t : LinearQuadtree, wsf : WSPairFuncType, dpf : DPairFuncType, dnf : DNodeFuncType, bc : BranchCondType) -> None:
		...

	@overload
	def __call__(self, u : NodeID) -> None:
		...

	@overload
	def __call__(self, u : NodeID, v : NodeID) -> None:
		...
