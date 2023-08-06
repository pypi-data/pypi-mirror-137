# file stubs/ogdf/IOPoints.py generated from classogdf_1_1_i_o_points
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
class IOPoints(object):

	"""Representation of in- and outpoint lists."""

	m_depth : NodeArray[  int ] = ...

	m_height : NodeArray[  int ] = ...

	@overload
	def __init__(self) -> None:
		...

	@overload
	def __init__(self, G : Graph) -> None:
		...

	def __destruct__(self) -> None:
		...

	def appendInpoint(self, adj : adjEntry) -> None:
		...

	def appendOutpoint(self, adj : adjEntry) -> None:
		...

	def changeEdge(self, v : node, adj_new : adjEntry) -> None:
		...

	def firstRealOut(self, v : node) -> ListConstIterator[InOutPoint]:
		...

	def _in(self, v : node) -> int:
		...

	def inLeft(self, v : node) -> int:
		...

	@overload
	def inpoints(self, v : node) -> List[InOutPoint]:
		...

	@overload
	def inpoints(self, v : node) -> List[InOutPoint]:
		...

	def inRight(self, v : node) -> int:
		...

	def isChain(self, v : node) -> bool:
		...

	def lastRealOut(self, v : node) -> ListConstIterator[InOutPoint]:
		...

	@overload
	def marked(self, adj : adjEntry) -> bool:
		...

	@overload
	def marked(self, v : node) -> bool:
		...

	def maxLeft(self, v : node) -> int:
		...

	def maxPlusLeft(self, v : node) -> int:
		...

	def maxPlusRight(self, v : node) -> int:
		...

	def maxRight(self, v : node) -> int:
		...

	def middleNeighbor(self, z1 : node) -> InOutPoint:
		...

	def nextRealOut(self, it : ListConstIterator[InOutPoint]) -> ListConstIterator[InOutPoint]:
		...

	def numDeg1(self, v : node, xl : int, xr : int, doubleCount : bool) -> None:
		...

	def out(self, v : node) -> int:
		...

	def outLeft(self, v : node) -> int:
		...

	@overload
	def outpoints(self, v : node) -> List[InOutPoint]:
		...

	@overload
	def outpoints(self, v : node) -> List[InOutPoint]:
		...

	def outRight(self, v : node) -> int:
		...

	def pointOf(self, adj : adjEntry) -> InOutPoint:
		...

	def prevRealOut(self, it : ListConstIterator[InOutPoint]) -> ListConstIterator[InOutPoint]:
		...

	def pushInpoint(self, adj : adjEntry) -> None:
		...

	def restoreDeg1Nodes(self, PG : PlanRep, S : ArrayBuffer[PlanRep.Deg1RestoreInfo]) -> None:
		...

	def setInCoord(self, it : ListIterator[InOutPoint], dx : int, dy : int) -> None:
		...

	def setOutCoord(self, it : ListIterator[InOutPoint], dx : int, dy : int) -> None:
		...

	def setOutDx(self, it : ListIterator[InOutPoint], dx : int) -> None:
		...

	def switchBeginIn(self, v : node) -> adjEntry:
		...

	def switchBeginOut(self, v : node) -> None:
		...

	def switchEndIn(self, v : node) -> adjEntry:
		...

	def switchEndOut(self, v : node) -> None:
		...
