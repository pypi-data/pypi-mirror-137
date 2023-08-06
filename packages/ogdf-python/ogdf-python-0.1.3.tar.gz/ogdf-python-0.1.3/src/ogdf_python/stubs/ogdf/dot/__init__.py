# file stubs/ogdf/dot/__init__.py generated from namespaceogdf_1_1dot
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
T = TypeVar('T')

G = TypeVar('G')

class dot(object):

	class Attribute(enum.Enum):

		Id = enum.auto()

		Label = enum.auto()

		Template = enum.auto()

		Stroke = enum.auto()

		Fill = enum.auto()

		StrokeType = enum.auto()

		Width = enum.auto()

		Height = enum.auto()

		Shape = enum.auto()

		Weight = enum.auto()

		DoubleWeight = enum.auto()

		Position = enum.auto()

		LabelPosition = enum.auto()

		Arrow = enum.auto()

		StrokeWidth = enum.auto()

		FillPattern = enum.auto()

		FillBackground = enum.auto()

		Type = enum.auto()

		Dir = enum.auto()

		SubGraphs = enum.auto()

		Unknown = enum.auto()

	def cross(self, G : ogdf.Graph, GA : GraphAttributes, _ : ClusterGraph, _ : ClusterGraphAttributes, defaults : List[Ast.AttrList], attrs : Ast.AttrList, lnodes : std.set[ogdf.node], rnodes : std.set[ogdf.node]) -> bool:
		...

	def destroyList(self, list : T) -> None:
		"""Frees a singly linked list without using recursion."""
		...

	@overload
	def readAttribute(self, CA : ClusterGraphAttributes, c : cluster, stmt : Ast.AsgnStmt) -> bool:
		...

	@overload
	def readAttribute(self, GA : GraphAttributes, e : edge, stmt : Ast.AsgnStmt) -> bool:
		...

	@overload
	def readAttribute(self, GA : GraphAttributes, v : node, stmt : Ast.AsgnStmt) -> bool:
		...

	@overload
	def readAttributes(self, GA : G, elem : T, attrs : Ast.AttrList) -> bool:
		...

	@overload
	def readAttributes(self, GA : G, elem : T, defaults : List[Ast.AttrList]) -> bool:
		...

	def readBends(self, str : str, polyline : DPolyline) -> bool:
		...

	def readStatements(self, P : Parser, G : Graph, GA : GraphAttributes, C : ClusterGraph, CA : ClusterGraphAttributes, data : SubgraphData, stmts : Ast.StmtList) -> bool:
		...

	def toArrow(self, str : str) -> EdgeArrow:
		...

	def toAttribute(self, str : str) -> Attribute:
		...

	def toEdgeType(self, str : str) -> Graph.EdgeType:
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
	def toString(self, shape : Shape) -> str:
		...

	def writeAttribute(self, out : std.ostream, separator : bool, name : str, value : T) -> None:
		...

	@overload
	def writeAttributes(self, out : std.ostream, CA : ClusterGraphAttributes, c : cluster) -> bool:
		...

	@overload
	def writeAttributes(self, out : std.ostream, GA : GraphAttributes, e : edge) -> None:
		...

	@overload
	def writeAttributes(self, out : std.ostream, GA : GraphAttributes, v : node) -> None:
		...

	def writeCluster(self, out : std.ostream, depth : int, edgeMap : ClusterArray[ List[edge] ], C : ClusterGraph, CA : ClusterGraphAttributes, c : cluster, clusterId : int) -> bool:
		...

	def writeEdge(self, out : std.ostream, depth : int, GA : GraphAttributes, e : edge) -> bool:
		...

	def writeGraph(self, out : std.ostream, G : Graph, GA : GraphAttributes) -> bool:
		...

	@overload
	def writeHeader(self, out : std.ostream, depth : int, CA : ClusterGraphAttributes, rootCluster : cluster, c : cluster, clusterId : int) -> bool:
		...

	@overload
	def writeHeader(self, out : std.ostream, depth : int, GA : GraphAttributes, writeAttributes : bool = True) -> bool:
		...

	def writeNode(self, out : std.ostream, depth : int, GA : GraphAttributes, v : node) -> bool:
		...
