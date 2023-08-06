# file stubs/ogdf/energybased/dtree/DTreeEmbedder/__init__.py generated from classogdf_1_1energybased_1_1dtree_1_1_d_tree_embedder
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
ForceFunc = TypeVar('ForceFunc')

AttrForceFunc = TypeVar('AttrForceFunc')

Dim = TypeVar('Dim')

UseForcePrime = TypeVar('UseForcePrime')

RepForceFunc = TypeVar('RepForceFunc')

class DTreeEmbedder(Generic[Dim]):

	def __init__(self, graph : Graph) -> None:
		"""constructor with a given graph, allocates memory and does initialization"""
		...

	def __destruct__(self) -> None:
		"""destructor"""
		...

	def centerNodesAt(self, centerBBox : float) -> None:
		"""computes the bounding box and all nodes are translated such that bbox center is at centerBBox"""
		...

	def computeEdgeForces(self, attrForceFunc : AttrForceFunc) -> None:
		"""computes the edge forces for one iteration"""
		...

	def computeRepForces(self, forceFunc : ForceFunc) -> None:
		"""computes the repulsive forces"""
		...

	def computeRepForcesApprox(self, forceFunc : ForceFunc) -> None:
		"""uses the tree code to approximate the repulsive forces in O(nlogn) for one iteration"""
		...

	def computeRepForcesExact(self, forceFunc : ForceFunc) -> None:
		"""computes the repulsive forces for one iteration in O(n^2)"""
		...

	def doIterationsNewton(self, numIterations : int, epsilon : float, repForceFunc : RepForceFunc, attrForceFunc : AttrForceFunc) -> None:
		...

	def doIterationsStandard(self, numIterations : int, epsilon : float, repForceFunc : RepForceFunc, attrForceFunc : AttrForceFunc) -> None:
		...

	def doIterationsTempl(self, numIterations : int, epsilon : float, repForceFunc : RepForceFunc, attrForceFunc : AttrForceFunc) -> None:
		"""does multiple iterations using the given repulsive force function"""
		...

	def edgeWeight(self, e : edge) -> float:
		"""returns the edge weight"""
		...

	def graph(self) -> Graph:
		"""returns the graph"""
		...

	def mass(self, v : node) -> float:
		"""returns the mass of node v"""
		...

	def moveNodes(self, timeStep : float) -> float:
		"""moves the nodes by the computed force vector"""
		...

	def moveNodesByForcePrime(self) -> float:
		...

	def position(self, v : node, d : int) -> float:
		"""returns the d-th coordinate of node v"""
		...

	def resetForces(self) -> None:
		"""sets the forces of all nodes to 0"""
		...

	def scaleNodes(self, scaleFactor : float) -> None:
		"""changes the position of nodes according to a given scale factor"""
		...

	def setEdgeWeight(self, e : edge, weight : float) -> None:
		"""sets the weight of an edge"""
		...

	def setMass(self, v : node, mass : float) -> None:
		"""sets the mass of a node v"""
		...

	def setPosition(self, v : node, d : int, coord : float) -> None:
		"""sets the d-th coordinate of node v to coord"""
		...
