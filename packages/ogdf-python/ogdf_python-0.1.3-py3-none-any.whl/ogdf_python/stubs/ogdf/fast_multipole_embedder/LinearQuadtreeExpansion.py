# file stubs/ogdf/fast_multipole_embedder/LinearQuadtreeExpansion.py generated from classogdf_1_1fast__multipole__embedder_1_1_linear_quadtree_expansion
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
class LinearQuadtreeExpansion(object):

	binCoef : BinCoeff[ float ] = ...

	#: the big local expansion coeff array
	m_localExp : float = ...

	#: the big multipole expansione coeff array
	m_multiExp : float = ...

	#: the number of coeff per expansions
	m_numCoeff : int = ...

	#: the number of multipole (locale) expansions
	m_numExp : int = ...

	def __init__(self, precision : int, tree : LinearQuadtree) -> None:
		"""constructor"""
		...

	def __destruct__(self, _ : None) -> None:
		"""destructor"""
		...

	def L2L(self, source : int, receiver : int) -> None:
		"""shifts the source local coefficient to the center of the receiver and adds them"""
		...

	def L2P(self, source : int, point : int, fx : float, fy : float) -> None:
		"""evaluates the derivate of the local expansion at the point and adds the forces to fx fy"""
		...

	def localExp(self) -> float:
		"""returns the array with local coefficients"""
		...

	def M2L(self, source : int, receiver : int) -> None:
		"""converts the source multipole coefficient in to a local coefficients at the center of the receiver and adds them"""
		...

	def M2M(self, source : int, receiver : int) -> None:
		"""shifts the source multipole coefficient to the center of the receiver and adds them"""
		...

	def multiExp(self) -> float:
		"""returns the array with multipole coefficients"""
		...

	def numCoeff(self) -> int:
		"""number of coefficients per expansions"""
		...

	def P2M(self, point : int, receiver : int) -> None:
		"""adds a point with the given charge to the receiver expansion"""
		...

	def sizeInBytes(self) -> int:
		"""returns the size in bytes"""
		...

	def tree(self) -> LinearQuadtree:
		"""the quadtree"""
		...
