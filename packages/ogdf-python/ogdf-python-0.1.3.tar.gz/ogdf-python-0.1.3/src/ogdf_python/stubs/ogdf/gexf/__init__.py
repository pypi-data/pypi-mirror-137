# file stubs/ogdf/gexf/__init__.py generated from namespaceogdf_1_1gexf
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
T = TypeVar('T')

class gexf(object):

	def defineAttribute(self, xmlNode : pugi.xml_node, name : str, type : str) -> None:
		...

	def defineAttributes(self, xmlNode : pugi.xml_node, GA : GraphAttributes) -> None:
		...

	def edgeNodes(self, v : node, id : str, clusterId : Dict[ str,cluster], nodes : List[node]) -> bool:
		...

	def readAttrDefs(self, attrMap : Dict[ str, str ], attrsTag : pugi.xml_node) -> bool:
		...

	@overload
	def readAttValue(self, GA : GraphAttributes, e : edge, name : str, value : str) -> None:
		...

	@overload
	def readAttValue(self, GA : GraphAttributes, v : node, name : str, value : str) -> None:
		...

	def readAttValues(self, GA : GraphAttributes, element : T, tag : pugi.xml_node, attrMap : Dict[ str, str ]) -> bool:
		...

	def readColor(self, color : Color, tag : pugi.xml_node) -> bool:
		...

	@overload
	def readVizAttribute(self, GA : GraphAttributes, e : edge, tag : pugi.xml_node) -> bool:
		...

	@overload
	def readVizAttribute(self, GA : GraphAttributes, v : node, tag : pugi.xml_node) -> bool:
		...

	def toGEXFStrokeType(self, type : StrokeType) -> str:
		...

	def toShape(self, str : str) -> Shape:
		...

	def toString(self, shape : Shape) -> str:
		...

	def toStrokeType(self, str : str) -> StrokeType:
		...

	@overload
	def writeAttributes(self, xmlNode : pugi.xml_node, GA : GraphAttributes, e : edge) -> None:
		...

	@overload
	def writeAttributes(self, xmlNode : pugi.xml_node, GA : GraphAttributes, v : node) -> None:
		...

	def writeAttValue(self, xmlNode : pugi.xml_node, attr : graphml.Attribute, value : T) -> None:
		...

	def writeCluster(self, rootNode : pugi.xml_node, C : ClusterGraph, CA : ClusterGraphAttributes, c : cluster) -> None:
		...

	def writeColor(self, xmlNode : pugi.xml_node, color : Color) -> None:
		...

	def writeEdge(self, xmlNode : pugi.xml_node, GA : GraphAttributes, e : edge) -> None:
		...

	def writeEdges(self, xmlNode : pugi.xml_node, G : Graph, GA : GraphAttributes) -> None:
		...

	def writeGraph(self, rootNode : pugi.xml_node, G : Graph, GA : GraphAttributes) -> None:
		...

	def writeHeader(self, doc : pugi.xml_document, viz : bool) -> pugi.xml_node:
		...

	def writeNode(self, xmlNode : pugi.xml_node, GA : GraphAttributes, v : node) -> None:
		...
