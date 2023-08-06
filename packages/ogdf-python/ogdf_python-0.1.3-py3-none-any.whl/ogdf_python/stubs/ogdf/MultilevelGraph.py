# file stubs/ogdf/MultilevelGraph.py generated from classogdf_1_1_multilevel_graph
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
class MultilevelGraph(object):

	@overload
	def __init__(self) -> None:
		...

	@overload
	def __init__(self, filename : str) -> None:
		...

	@overload
	def __init__(self, G : Graph) -> None:
		...

	@overload
	def __init__(self, GA : GraphAttributes) -> None:
		...

	@overload
	def __init__(self, GA : GraphAttributes, G : Graph) -> None:
		...

	@overload
	def __init__(self, _is : std.istream) -> None:
		...

	def __destruct__(self) -> None:
		...

	def averageRadius(self) -> float:
		...

	def changeEdge(self, NM : NodeMerge, theEdge : edge, newWeight : float, newSource : node, newTarget : node) -> bool:
		...

	def changeNode(self, NM : NodeMerge, theNode : node, newRadius : float, merged : node) -> bool:
		...

	def copyEdgeTo(self, e : edge, MLG : MultilevelGraph, tempNodeAssociations : Dict[node,node], associate : bool, index : int = -1) -> None:
		...

	def copyNodeTo(self, v : node, MLG : MultilevelGraph, tempNodeAssociations : Dict[node,node], associate : bool, index : int = -1) -> None:
		...

	def deleteEdge(self, NM : NodeMerge, theEdge : edge) -> bool:
		...

	def exportAttributes(self, GA : GraphAttributes) -> None:
		...

	def exportAttributesSimple(self, GA : GraphAttributes) -> None:
		...

	def getEdge(self, index : int) -> edge:
		...

	def getGraph(self) -> Graph:
		...

	def getGraphAttributes(self) -> GraphAttributes:
		"""Returns attributes of current level graph asGraphAttributes."""
		...

	def getLastMerge(self) -> NodeMerge:
		...

	def getLevel(self) -> int:
		...

	def getNode(self, index : int) -> node:
		...

	def getRArray(self) -> NodeArray[ float ]:
		...

	def getWArray(self) -> EdgeArray[ float ]:
		...

	def importAttributes(self, GA : GraphAttributes) -> None:
		...

	def importAttributesSimple(self, GA : GraphAttributes) -> None:
		...

	def mergeWeight(self, v : node) -> int:
		...

	def moveEdgesToParent(self, NM : NodeMerge, theNode : node, parent : node, deleteDoubleEndges : bool, adjustEdgeLengths : int) -> List[edge]:
		...

	def moveToZero(self) -> None:
		...

	def postMerge(self, NM : NodeMerge, merged : node) -> bool:
		...

	@overload
	def radius(self, v : node) -> float:
		...

	@overload
	def radius(self, v : node, r : float) -> None:
		...

	def reInsertAll(self, components : List[MultilevelGraph]) -> None:
		...

	def reInsertGraph(self, MLG : MultilevelGraph) -> None:
		...

	def splitIntoComponents(self) -> List[MultilevelGraph]:
		...

	def undoLastMerge(self) -> node:
		...

	def updateMergeWeights(self) -> None:
		...

	def updateReverseIndizes(self) -> None:
		...

	@overload
	def weight(self, e : edge) -> float:
		...

	@overload
	def weight(self, e : edge, weight : float) -> None:
		...

	@overload
	def writeGML(self, fileName : str) -> None:
		...

	@overload
	def writeGML(self, os : std.ostream) -> None:
		...

	@overload
	def x(self, v : node) -> float:
		...

	@overload
	def x(self, v : node, x : float) -> None:
		...

	@overload
	def y(self, v : node) -> float:
		...

	@overload
	def y(self, v : node, y : float) -> None:
		...
