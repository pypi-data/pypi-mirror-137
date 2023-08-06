# file stubs/ogdf/ComputeTricOrder.py generated from classogdf_1_1_compute_tric_order
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
class ComputeTricOrder(object):

	def __init__(self, G : Graph, E : ConstCombinatorialEmbedding, outerFace : face, preferNodes : bool = False) -> None:
		...

	def addOuterNode(self, v : node, f : face) -> None:
		...

	def decSepf(self, v : node) -> None:
		...

	def doUpdate(self) -> None:
		...

	def getNextPossible(self, v : node, f : face) -> None:
		...

	def getOuterNodeDeg2(self, f : face, adjPred : NodeArray[adjEntry], adjSucc : NodeArray[adjEntry]) -> node:
		...

	def getOutv(self, f : face) -> int:
		...

	def incOute(self, f : face) -> None:
		...

	def incOutv(self, f : face) -> None:
		...

	def incSepf(self, v : node) -> None:
		...

	def incVisited(self, v : node) -> None:
		...

	def initOuterEdges(self) -> None:
		...

	def initOuterNodes(self, v1 : node, v2 : node) -> None:
		...

	def initPossible(self, v : node) -> None:
		...

	def isNode(self) -> bool:
		...

	def isOnlyEdge(self, f : face) -> bool:
		...

	def isPossible(self) -> bool:
		...

	def output(self) -> None:
		...
