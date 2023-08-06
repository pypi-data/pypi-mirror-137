# file stubs/ogdf/gdf/__init__.py generated from namespaceogdf_1_1gdf
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
T = TypeVar('T')

Attr = TypeVar('Attr')

A = TypeVar('A')

class gdf(object):

	class EdgeAttribute(enum.Enum):

		Label = enum.auto()

		Source = enum.auto()

		Target = enum.auto()

		Weight = enum.auto()

		Directed = enum.auto()

		Color = enum.auto()

		Bends = enum.auto()

		Unknown = enum.auto()

	class NodeAttribute(enum.Enum):

		Name = enum.auto()

		Label = enum.auto()

		X = enum.auto()

		Y = enum.auto()

		Z = enum.auto()

		FillColor = enum.auto()

		FillPattern = enum.auto()

		StrokeColor = enum.auto()

		StrokeType = enum.auto()

		StrokeWidth = enum.auto()

		Shape = enum.auto()

		Width = enum.auto()

		Height = enum.auto()

		Template = enum.auto()

		Weight = enum.auto()

		FillBgColor = enum.auto()

		Unknown = enum.auto()

	def match(self, text : str, pattern : str) -> size_t:
		...

	@overload
	def readAttribute(self, GA : GraphAttributes, e : edge, attr : EdgeAttribute, value : str) -> bool:
		...

	@overload
	def readAttribute(self, GA : GraphAttributes, v : node, attr : NodeAttribute, value : str) -> bool:
		...

	def readAttrs(self, GA : GraphAttributes, elem : T, attrs : List[ A ], values : List[ str ]) -> bool:
		...

	def readDef(self, str : str, toAttribute : Attr, a_unknown : Attr, attrs : List[ Attr ]) -> bool:
		...

	def scanQuoted(self, str : str, pos : size_t, buff : str) -> size_t:
		...

	def split(self, str : str, result : List[ str ]) -> bool:
		...

	def toColor(self, str : str) -> Color:
		...

	def toEdgeAttribute(self, str : str) -> EdgeAttribute:
		...

	def toNodeAttribute(self, str : str) -> NodeAttribute:
		...

	def toShape(self, str : str) -> Shape:
		...

	@overload
	def toString(self, attr : EdgeAttribute) -> str:
		...

	@overload
	def toString(self, attr : NodeAttribute) -> str:
		...

	@overload
	def toString(self, shape : Shape) -> str:
		...

	def writeColor(self, os : std.ostream, color : Color) -> None:
		...

	def writeEdge(self, os : std.ostream, GA : GraphAttributes, e : edge) -> None:
		...

	def writeEdgeHeader(self, os : std.ostream, GA : GraphAttributes) -> None:
		...

	def writeGraph(self, os : std.ostream, G : Graph, GA : GraphAttributes) -> None:
		...

	def writeNode(self, os : std.ostream, GA : GraphAttributes, v : node) -> None:
		...

	def writeNodeHeader(self, os : std.ostream, GA : GraphAttributes) -> None:
		...
