# file stubs/ogdf/PALabel.py generated from classogdf_1_1_p_a_label
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
class PALabel(object):

	"""auxiliary class for the planar augmentation algorithm"""

	class StopCause(enum.Enum):

		Planarity = enum.auto()

		CDegree = enum.auto()

		BDegree = enum.auto()

		Root = enum.auto()

	def __init__(self, parent : node, cutvertex : node, sc : StopCause = StopCause.BDegree) -> None:
		...

	def addPendant(self, pendant : node) -> None:
		...

	def deleteAllPendants(self) -> None:
		...

	def getFirstPendant(self) -> node:
		...

	def getLastPendant(self) -> node:
		...

	def getPendant(self, nr : int) -> node:
		"""return pendant with number nr, starts counting at 0"""
		...

	def head(self) -> node:
		"""returns the head node"""
		...

	def isBLabel(self) -> bool:
		...

	def isCLabel(self) -> bool:
		...

	def parent(self) -> node:
		"""return the parent node. If the label is a c-label it returns m_head"""
		...

	def removeFirstPendant(self) -> None:
		...

	@overload
	def removePendant(self, it : ListIterator[node]) -> None:
		...

	@overload
	def removePendant(self, pendant : node) -> None:
		...

	def setHead(self, newHead : node) -> None:
		...

	def setParent(self, newParent : node) -> None:
		...

	def size(self) -> int:
		"""return number of pendants"""
		...

	@overload
	def stopCause(self) -> StopCause:
		...

	@overload
	def stopCause(self, sc : StopCause) -> None:
		...
