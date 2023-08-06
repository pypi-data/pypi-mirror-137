# file stubs/ogdf/fast_multipole_embedder/LinearQuadtree/__init__.py generated from classogdf_1_1fast__multipole__embedder_1_1_linear_quadtree
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
F = TypeVar('F')

Cond = TypeVar('Cond')

A = TypeVar('A')

C = TypeVar('C')

B = TypeVar('B')

ConditionType = TypeVar('ConditionType')

Func = TypeVar('Func')

class LinearQuadtree(object):

	NodeID : Type = int

	PointID : Type = int

	def __init__(self, n : int, origXPos : float, origYPos : float, origSize : float) -> None:
		"""constructor. required tree mem will be allocated"""
		...

	def __destruct__(self, _ : None) -> None:
		"""destructor. tree mem will be released"""
		...

	@overload
	def bottom_up_traversal(self, f : F) -> bottom_up_traversal_functor[ F ]:
		"""creator"""
		...

	@overload
	def bottom_up_traversal(self, f : F, cond : Cond) -> bottom_up_traversal_functor[ F, Cond ]:
		"""creator"""
		...

	def child(self, nodeID : NodeID, i : int) -> NodeID:
		"""returns theith child index of nodenodeID"""
		...

	def clear(self) -> None:
		"""resets the tree"""
		...

	def computeCoords(self, nodeIndex : NodeID) -> None:
		...

	@overload
	def computeWSPD(self) -> None:
		...

	@overload
	def computeWSPD(self, n : NodeID) -> None:
		...

	def directNode(self, i : int) -> NodeID:
		...

	def directNodeA(self, i : int) -> NodeID:
		...

	def directNodeB(self, i : int) -> NodeID:
		...

	def findFirstPointInCell(self, somePointInCell : PointID) -> PointID:
		"""iterates back in the sequence until the first point with another morton number occures, returns that point +1"""
		...

	def firstInnerNode(self) -> NodeID:
		...

	def firstLeaf(self) -> NodeID:
		...

	def firstPoint(self, nodeID : NodeID) -> PointID:
		...

	def forall_children(self, f : F) -> forall_children_functor[ F ]:
		"""creator"""
		...

	def forall_ordered_pairs_of_children(self, f : F) -> forall_ordered_pairs_of_children_functor[ F ]:
		"""creator"""
		...

	def forall_points(self, func : Func) -> forall_points_functor[ Func ]:
		"""creator"""
		...

	def forall_tree_nodes(self, f : F, begin : NodeID, num : int) -> forall_tree_nodes_functor[ F ]:
		"""creator"""
		...

	@overload
	def forall_well_separated_pairs(self, a : A, b : B, c : C) -> wspd_functor[ A, B, C ]:
		...

	@overload
	def forall_well_separated_pairs(self, a : A, b : B, c : C, cond : ConditionType) -> wspd_functor[ A, B, C, ConditionType ]:
		...

	def init(self, min_x : float, min_y : float, max_x : float, max_y : float) -> None:
		...

	def is_fence_condition(self) -> is_fence_condition_functor:
		"""creator"""
		...

	def is_leaf_condition(self) -> is_leaf_condition_functor:
		"""creator"""
		...

	def isFence(self, nodeID : NodeID) -> bool:
		"""sets the fence flag for nodenodeID"""
		...

	def isLeaf(self, nodeID : NodeID) -> bool:
		"""returns true if the given node index is a leaf"""
		...

	def isWS(self, a : NodeID, b : NodeID) -> bool:
		...

	def level(self, nodeID : NodeID) -> NodeID:
		...

	def maxNumberOfNodes(self) -> int:
		"""the upper bound for a compressed quadtree (2*numPoints)"""
		...

	def maxX(self) -> float:
		...

	def maxY(self) -> float:
		...

	def minX(self) -> float:
		...

	def minY(self) -> float:
		...

	def mortonNr(self, point : PointID) -> MortonNR:
		...

	def nextNode(self, nodeID : NodeID) -> NodeID:
		...

	def nodeFence(self, nodeID : NodeID) -> None:
		...

	def nodeOfPoint(self, id : PointID) -> NodeID:
		...

	def nodeSize(self, nodeID : NodeID) -> float:
		...

	def nodeX(self, nodeID : NodeID) -> float:
		...

	def nodeY(self, nodeID : NodeID) -> float:
		...

	def numberOfChilds(self, nodeID : NodeID) -> int:
		"""returns the number of children of nodenodeID. for an inner node this is 1..4 and can be accessed by child(i). For a leaf the number of points in this leaf is returned starting with point child(0)"""
		...

	def numberOfDirectNodes(self) -> int:
		...

	def numberOfDirectPairs(self) -> int:
		...

	def numberOfInnerNodes(self) -> int:
		...

	def numberOfLeaves(self) -> int:
		...

	def numberOfNodes(self) -> int:
		"""returns the number of nodes in this tree"""
		...

	@overload
	def numberOfPoints(self) -> int:
		"""returns the number of points in this tree"""
		...

	@overload
	def numberOfPoints(self, nodeID : NodeID) -> int:
		"""returns the number of points contained in the subtree of nodenodeID"""
		...

	def numberOfWSP(self) -> int:
		...

	@overload
	def point(self, pointID : PointID) -> LQPoint:
		...

	@overload
	def point(self, pointID : PointID) -> LQPoint:
		...

	def pointArray(self) -> LQPoint:
		...

	def pointLeaf(self, point : PointID) -> NodeID:
		...

	@overload
	def pointSize(self) -> float:
		...

	@overload
	def pointSize(self, point : PointID) -> float:
		...

	@overload
	def pointX(self) -> float:
		...

	@overload
	def pointX(self, point : PointID) -> float:
		...

	@overload
	def pointY(self) -> float:
		...

	@overload
	def pointY(self, point : PointID) -> float:
		...

	def refOfPoint(self, id : PointID) -> int:
		...

	def root(self) -> NodeID:
		"""returns the index of the root"""
		...

	def scaleInv(self) -> float:
		...

	def setChild(self, nodeID : NodeID, i : int, c : NodeID) -> None:
		"""sets theith child index of nodenodeID"""
		...

	def setFirstPoint(self, nodeID : NodeID, firstPoint : PointID) -> None:
		...

	def setLevel(self, nodeID : NodeID, level : int) -> None:
		...

	def setNextNode(self, nodeID : NodeID, next : NodeID) -> None:
		...

	def setNodeSize(self, nodeID : NodeID, size : float) -> None:
		...

	def setNodeX(self, nodeID : NodeID, x : float) -> None:
		...

	def setNodeY(self, nodeID : NodeID, y : float) -> None:
		...

	def setNumberOfChilds(self, nodeID : NodeID, numChilds : int) -> None:
		"""sets the number of children of a node"""
		...

	def setNumberOfPoints(self, nodeID : NodeID, numPoints : int) -> None:
		"""sets the number of nodes containted in nodenodeID"""
		...

	@overload
	def setPoint(self, id : PointID, x : float, y : float, r : float) -> None:
		...

	@overload
	def setPoint(self, id : PointID, x : float, y : float, r : float, ref : int) -> None:
		...

	@overload
	def setPoint(self, id : PointID, x : float, y : float, ref : int) -> None:
		...

	def setPointLeaf(self, point : PointID, leaf : NodeID) -> None:
		...

	def sizeInBytes(self) -> int:
		...

	def StoreDirectNodeFunction(self) -> StoreDirectNodeFunctor:
		...

	def StoreDirectPairFunction(self) -> StoreDirectPairFunctor:
		...

	def StoreWSPairFunction(self) -> StoreWSPairFunctor:
		...

	@overload
	def top_down_traversal(self, f : F) -> top_down_traversal_functor[ F ]:
		"""creator"""
		...

	@overload
	def top_down_traversal(self, f : F, cond : Cond) -> top_down_traversal_functor[ F, Cond ]:
		"""creator"""
		...

	def updatePointPositionSize(self, id : PointID) -> None:
		...

	def wspd(self) -> WSPD:
		...
