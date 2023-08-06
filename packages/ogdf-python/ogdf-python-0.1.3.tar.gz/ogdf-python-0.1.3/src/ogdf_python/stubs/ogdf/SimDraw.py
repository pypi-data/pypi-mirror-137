# file stubs/ogdf/SimDraw.py generated from classogdf_1_1_sim_draw
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
class SimDraw(object):

	"""The Base class for simultaneous graph drawing."""

	class CompareBy(enum.Enum):

		"""Types for node comparison."""

		#: nodes are compared by their indices
		index = enum.auto()

		#: nodes are compared by their labels
		label = enum.auto()

	def __init__(self) -> None:
		"""constructs empty simdraw instance"""
		...

	def addAttribute(self, attr : int) -> None:
		"""gives access to new attribute if not already given"""
		...

	def addGraph(self, G : Graph) -> bool:
		"""adds the graph g to the instance m_G"""
		...

	def addGraphAttributes(self, GA : GraphAttributes) -> bool:
		"""adds newGraphAttributesto m_G"""
		...

	def clear(self) -> None:
		"""empty graph"""
		...

	@overload
	def compareBy(self) -> CompareBy:
		"""returns compare mode"""
		...

	@overload
	def compareBy(self) -> CompareBy:
		"""returns compare mode"""
		...

	@overload
	def constGraph(self) -> Graph:
		"""returns graph"""
		...

	@overload
	def constGraph(self) -> Graph:
		"""returns graph"""
		...

	@overload
	def constGraphAttributes(self) -> GraphAttributes:
		"""returns graphattributes"""
		...

	@overload
	def constGraphAttributes(self) -> GraphAttributes:
		"""returns graphattributes"""
		...

	def getBasicGraph(self, i : int) -> Graph:
		"""returns graph consisting of all edges and nodes from SubGraphi"""
		...

	def getBasicGraphAttributes(self, i : int, GA : GraphAttributes, G : Graph) -> None:
		"""returns graphattributes associated with basic graphi"""
		...

	@overload
	def isDummy(self, v : node) -> bool:
		"""returns true if nodevis marked as dummy"""
		...

	@overload
	def isDummy(self, v : node) -> bool:
		"""returns true if nodevis marked as dummy"""
		...

	def isPhantomDummy(self, v : node) -> bool:
		"""returns true if nodevis a cost zero dummy node"""
		...

	def isProperDummy(self, v : node) -> bool:
		"""returns true if nodevis a cost greater zero dummy node"""
		...

	def maxSubGraph(self) -> int:
		"""calculates maximum number of input graphs"""
		...

	def numberOfBasicGraphs(self) -> int:
		"""returns number of BasicGraphs in m_G"""
		...

	def numberOfDummyNodes(self) -> int:
		"""returns number of dummy nodes"""
		...

	def numberOfNodes(self) -> int:
		"""returns number of nodes"""
		...

	def numberOfPhantomDummyNodes(self) -> int:
		"""returns number of phantom dummy nodes"""
		...

	def numberOfProperDummyNodes(self) -> int:
		"""returns number of proper dummy nodes"""
		...

	def readGML(self, fileName : str) -> None:
		"""calls GraphAttributes::readGML"""
		...

	def writeGML(self, fileName : str) -> None:
		"""calls GraphAttributes::writeGML"""
		...
