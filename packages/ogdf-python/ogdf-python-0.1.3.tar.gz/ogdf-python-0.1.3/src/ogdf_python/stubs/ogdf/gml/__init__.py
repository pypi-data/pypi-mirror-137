# file stubs/ogdf/gml/__init__.py generated from namespaceogdf_1_1gml
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
class gml(object):

	class Key(enum.Enum):

		Id = enum.auto()

		Label = enum.auto()

		Creator = enum.auto()

		Name = enum.auto()

		Graph = enum.auto()

		Version = enum.auto()

		Directed = enum.auto()

		Node = enum.auto()

		Edge = enum.auto()

		Graphics = enum.auto()

		X = enum.auto()

		Y = enum.auto()

		Z = enum.auto()

		W = enum.auto()

		H = enum.auto()

		Type = enum.auto()

		Width = enum.auto()

		Source = enum.auto()

		Target = enum.auto()

		Arrow = enum.auto()

		Outline = enum.auto()

		Point = enum.auto()

		Bends = enum.auto()

		Generalization = enum.auto()

		SubGraph = enum.auto()

		Fill = enum.auto()

		FillBg = enum.auto()

		Cluster = enum.auto()

		Root = enum.auto()

		Vertex = enum.auto()

		Color = enum.auto()

		Height = enum.auto()

		Stipple = enum.auto()

		Pattern = enum.auto()

		LineWidth = enum.auto()

		Template = enum.auto()

		Weight = enum.auto()

		EdgeIntWeight = enum.auto()

		Unknown = enum.auto()

	class ObjectType(enum.Enum):

		IntValue = enum.auto()

		DoubleValue = enum.auto()

		StringValue = enum.auto()

		ListBegin = enum.auto()

		ListEnd = enum.auto()

		Key = enum.auto()

		Eof = enum.auto()

		Error = enum.auto()

	def toArrow(self, str : str) -> EdgeArrow:
		...

	def toKey(self, str : str) -> Key:
		...

	def toNodeType(self, str : str) -> Graph.NodeType:
		...

	@overload
	def toString(self, arrow : EdgeArrow) -> str:
		...

	@overload
	def toString(self, type : Graph.NodeType) -> str:
		...

	@overload
	def toString(self, attr : Key) -> str:
		...

	@overload
	def toString(self, type : ObjectType) -> str:
		...
