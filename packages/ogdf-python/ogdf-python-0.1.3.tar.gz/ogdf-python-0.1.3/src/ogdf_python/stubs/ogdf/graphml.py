# file stubs/ogdf/graphml.py generated from namespaceogdf_1_1graphml
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
class graphml(object):

	class Attribute(enum.Enum):

		NodeLabel = enum.auto()

		EdgeLabel = enum.auto()

		X = enum.auto()

		Y = enum.auto()

		Z = enum.auto()

		Width = enum.auto()

		Height = enum.auto()

		Size = enum.auto()

		Shape = enum.auto()

		NodeLabelX = enum.auto()

		NodeLabelY = enum.auto()

		NodeLabelZ = enum.auto()

		NodeStrokeColor = enum.auto()

		NodeStrokeType = enum.auto()

		NodeStrokeWidth = enum.auto()

		EdgeStrokeColor = enum.auto()

		EdgeStrokeType = enum.auto()

		EdgeStrokeWidth = enum.auto()

		ClusterStroke = enum.auto()

		NodeFillPattern = enum.auto()

		NodeFillBackground = enum.auto()

		R = enum.auto()

		G = enum.auto()

		B = enum.auto()

		NodeWeight = enum.auto()

		EdgeWeight = enum.auto()

		NodeType = enum.auto()

		EdgeType = enum.auto()

		NodeId = enum.auto()

		Template = enum.auto()

		EdgeArrow = enum.auto()

		EdgeSubGraph = enum.auto()

		EdgeBends = enum.auto()

		Unknown = enum.auto()

	def toArrow(self, str : str) -> EdgeArrow:
		...

	def toAttribute(self, str : str) -> Attribute:
		...

	def toEdgeType(self, str : str) -> Graph.EdgeType:
		...

	def toNodeType(self, str : str) -> Graph.NodeType:
		...

	def toShape(self, str : str) -> Shape:
		...

	@overload
	def toString(self, attr : Attribute) -> str:
		...

	@overload
	def toString(self, arrow : EdgeArrow) -> str:
		...

	@overload
	def toString(self, type : Graph.EdgeType) -> str:
		...

	@overload
	def toString(self, type : Graph.NodeType) -> str:
		...

	@overload
	def toString(self, shape : Shape) -> str:
		...
