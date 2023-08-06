# file stubs/ogdf/tlp/__init__.py generated from namespaceogdf_1_1tlp
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
GraphE = TypeVar('GraphE')

Type = TypeVar('Type')

class tlp(object):

	class Attribute(enum.Enum):

		label = enum.auto()

		color = enum.auto()

		strokeColor = enum.auto()

		strokeWidth = enum.auto()

		strokeType = enum.auto()

		fillPattern = enum.auto()

		fillBackground = enum.auto()

		position = enum.auto()

		size = enum.auto()

		shape = enum.auto()

		unknown = enum.auto()

	def clusterCompare(self, a : node, b : node) -> bool:
		...

	def getClusterChildren(self, c : cluster, nodes : List[node]) -> None:
		...

	def __lshift__(self, os : std.ostream, token : Token) -> std.ostream:
		...

	@overload
	def setAttribute(self, GA : GraphAttributes, e : edge, attr : Attribute, value : str) -> bool:
		...

	@overload
	def setAttribute(self, GA : GraphAttributes, v : node, attr : Attribute, value : str) -> bool:
		...

	def toAttribute(self, str : str) -> Attribute:
		...

	def toString(self, attr : Attribute) -> str:
		...

	def writeCluster(self, os : std.ostream, depth : int, G : Graph, C : ClusterGraph, c : cluster) -> None:
		...

	def writeColor(self, c : Color) -> str:
		...

	def writeEdges(self, os : std.ostream, G : Graph) -> None:
		...

	def writeGraph(self, os : std.ostream, G : Graph, C : ClusterGraph, GA : GraphAttributes) -> None:
		...

	def writeNodes(self, os : std.ostream, G : Graph) -> None:
		...

	def writeProperties(self, os : std.ostream, G : Graph, GA : GraphAttributes) -> None:
		...

	def writePropertyHeader(self, os : std.ostream, attr : Attribute, type : str) -> None:
		...

	def writeRange(self, os : std.ostream, a : int, b : int) -> None:
		...

	def writeSingleProperty(self, os : std.ostream, ga : Callable, graphElements : List[ GraphE ], GraphEName : str, attribute : Attribute, attrName : str, defaultValue : Type, printDefault : bool, toString : Callable) -> None:
		...
