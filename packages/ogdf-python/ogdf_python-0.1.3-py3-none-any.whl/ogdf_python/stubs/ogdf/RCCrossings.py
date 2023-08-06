# file stubs/ogdf/RCCrossings.py generated from structogdf_1_1_r_c_crossings
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
class RCCrossings(object):

	m_cnClusters : int = ...

	m_cnEdges : int = ...

	@overload
	def __init__(self) -> None:
		...

	@overload
	def __init__(self, cnClusters : int, cnEdges : int) -> None:
		...

	def incClusters(self) -> None:
		...

	def incEdges(self, cn : int) -> None:
		...

	def isZero(self) -> bool:
		...

	def __add__(self, cr : RCCrossings) -> RCCrossings:
		...

	def __iadd__(self, cr : RCCrossings) -> RCCrossings:
		...

	def __sub__(self, cr : RCCrossings) -> RCCrossings:
		...

	def __lt__(self, cr : RCCrossings) -> bool:
		...

	def __le__(self, cr : RCCrossings) -> bool:
		...

	def setInfinity(self) -> RCCrossings:
		...

	def compare(self, x : RCCrossings, y : RCCrossings) -> int:
		...
