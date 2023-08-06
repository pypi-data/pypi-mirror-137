# file stubs/ogdf/ComputeBicOrder.py generated from classogdf_1_1_compute_bic_order
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
class ComputeBicOrder(object):

	class CandidateType(enum.Enum):

		Face = enum.auto()

		Node = enum.auto()

		Edge = enum.auto()

	def __init__(self, G : Graph, E : ConstCombinatorialEmbedding, extFace : face, baseRatio : float) -> None:
		...

	def cutv(self, f : face) -> bool:
		...

	def doUpdate(self) -> None:
		...

	def externalFace(self) -> face:
		...

	def getPossible(self) -> bool:
		...

	def initPossibles(self) -> None:
		...

	def isPossFace(self, f : face) -> bool:
		...

	def isPossNode(self, v : node) -> bool:
		...

	def isPossVirt(self, v : node) -> bool:
		...

	@overload
	def left(self, adj : adjEntry) -> face:
		...

	@overload
	def left(self, v : node) -> face:
		...

	def next(self, v : node) -> node:
		...

	def nextPoss(self) -> CandidateType:
		...

	def prev(self, v : node) -> node:
		...

	def print(self) -> None:
		...

	def removeNextFace(self, V : ShellingOrderSet) -> None:
		...

	def removeNextNode(self, V : ShellingOrderSet) -> None:
		...

	def removeNextVirt(self, V : ShellingOrderSet) -> None:
		...

	@overload
	def right(self, adj : adjEntry) -> face:
		...

	@overload
	def right(self, v : node) -> face:
		...

	def setV1(self, V : ShellingOrderSet) -> None:
		...

	def virte(self, v : node) -> int:
		...
