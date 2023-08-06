# file stubs/ogdf/energybased/dtree/DTreeWSPD/__init__.py generated from classogdf_1_1energybased_1_1dtree_1_1_d_tree_w_s_p_d
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
Dim = TypeVar('Dim')

class DTreeWSPD(Generic[Dim]):

	IntType : Type = int

	Tree : Type = DTree[IntType, Dim ]

	#: the bounding box max coord of the point set
	m_bboxMax : float = ...

	#: the bounding box min coord of the point set
	m_bboxMin : float = ...

	#: geometry for the quadtree nodes
	m_nodeData : NodeData = ...

	#: number of points
	m_numPoints : int = ...

	m_pIWSPD : IWSPD = ...

	#: point data
	m_pointData : PointData = ...

	#: the quadtree this wspd is working on
	m_pTree : Tree = ...

	#: the separation factor for the ws predicate
	m_wspdSeparationFactor : float = ...

	#: a cached value for the ws test
	m_wspdSeparationFactorPlus2Squared_cached : float = ...

	def __init__(self, numPoints : int) -> None:
		"""constructs a new WSPD for numPoints"""
		...

	def __destruct__(self) -> None:
		"""destructor"""
		...

	def computeWSPD(self, m_pIWSPD : IWSPD) -> None:
		...

	@overload
	def node(self, i : int) -> NodeData:
		"""returns the data for a quadtree"""
		...

	def point(self, i : int) -> PointData:
		"""return ith point"""
		...

	def separationFactor(self) -> float:
		"""returns the parameter s of the WSPD (default is 1.0)"""
		...

	def setPoint(self, i : int, d : int, coord : float) -> None:
		"""sets the point to the given coords"""
		...

	def setSeparationFactor(self, s : float) -> None:
		"""sets the parameter s of the WSPD (default is 1.0)"""
		...

	def tree(self) -> Tree:
		"""returns the corresponding Dtree"""
		...

	def update(self) -> None:
		"""call this when the point set has been updated."""
		...

	def allocate(self) -> None:
		"""allocate mem"""
		...

	@overload
	def areWellSeparated(self, a : int, b : int) -> bool:
		"""predicate for determining if cells are well-separated"""
		...

	@overload
	def areWellSeparated(self, a : int, b : int) -> bool:
		...

	@overload
	def areWellSeparated(self, a : int, b : int) -> bool:
		...

	def deallocate(self) -> None:
		"""free mem"""
		...

	@overload
	def node(self, i : int) -> NodeData:
		"""returns the data for a quadtree"""
		...

	def updateBoundingBox(self) -> None:
		"""updates the bounding box by iterating over all points"""
		...

	def updateTreeGridPoints(self) -> None:
		"""updates the integer grid points in the quadtree"""
		...

	@overload
	def updateTreeNodeGeometry(self) -> None:
		"""updates the geometry of the quadtree nodes"""
		...

	@overload
	def updateTreeNodeGeometry(self, curr : int) -> None:
		"""the recursive function of the above"""
		...

	@overload
	def wspdRecursive(self, a : int) -> None:
		"""the unary recursive function generating the binary calls"""
		...

	@overload
	def wspdRecursive(self, a : int, b : int) -> None:
		"""the binary recursive function to separate the subtree a and b"""
		...
