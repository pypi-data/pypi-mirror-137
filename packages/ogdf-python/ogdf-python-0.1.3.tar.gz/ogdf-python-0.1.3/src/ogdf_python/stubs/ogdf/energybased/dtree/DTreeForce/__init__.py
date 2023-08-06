# file stubs/ogdf/energybased/dtree/DTreeForce/__init__.py generated from classogdf_1_1energybased_1_1dtree_1_1_d_tree_force
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
Dim = TypeVar('Dim')

UseForcePrime = TypeVar('UseForcePrime')

ForceFunc = TypeVar('ForceFunc')

class DTreeForce(Generic[Dim]):

	Tree : Type = WSPD.Tree

	WSPD : Type = DTreeWSPD[ Dim ]

	def __init__(self, numPoints : int) -> None:
		"""constructs a new WSPD (well-separated pair decomposition) for numPoints"""
		...

	def __destruct__(self) -> None:
		"""destructor"""
		...

	def computeForces(self, forceFunc : ForceFunc) -> None:
		"""main call"""
		...

	def force(self, i : int, d : int) -> float:
		"""returns d-th coordinate of the i-th force vector"""
		...

	def force_prime(self, i : int) -> float:
		"""returns derivation of the d-th coordinate of the i-th force vector"""
		...

	def mass(self, i : int) -> float:
		"""returns the mass of the i-th point"""
		...

	def numPoints(self) -> int:
		"""returns the number of points"""
		...

	def position(self, i : int, d : int) -> float:
		"""returns d-th coordinate of the i-th point"""
		...

	def setMass(self, i : int, m : float) -> None:
		"""sets the mass of the i-th point"""
		...

	def setPosition(self, i : int, d : int, c : float) -> None:
		"""sets the d-th coordinate of the i-th point"""
		...

	def tree(self) -> Tree:
		"""returns a const reference to the tree"""
		...

	def wspd(self) -> WSPD:
		"""returns a const ref to the wspd"""
		...
