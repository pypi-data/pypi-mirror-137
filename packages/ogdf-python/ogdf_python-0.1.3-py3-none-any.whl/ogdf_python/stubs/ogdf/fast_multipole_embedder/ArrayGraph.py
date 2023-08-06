# file stubs/ogdf/fast_multipole_embedder/ArrayGraph.py generated from classogdf_1_1fast__multipole__embedder_1_1_array_graph
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
LengthType = TypeVar('LengthType')

SizeType = TypeVar('SizeType')

CoordinateType = TypeVar('CoordinateType')

class ArrayGraph(object):

	@overload
	def __init__(self) -> None:
		"""Constructor. Does not allocate memory for the members."""
		...

	@overload
	def __init__(self, GA : GraphAttributes, edgeLength : EdgeArray[ float ], nodeSize : NodeArray[ float ]) -> None:
		"""Constructor."""
		...

	@overload
	def __init__(self, maxNumNodes : int, maxNumEdges : int) -> None:
		"""Constructor. Allocates memory via OGDF_MALLOC_16."""
		...

	def __destruct__(self) -> None:
		"""Destructor. Deallocates the memory via OGDF_FREE_16 if needed."""
		...

	def avgDesiredEdgeLength(self) -> float:
		"""Average edge length."""
		...

	def avgNodeSize(self) -> float:
		"""Average node size."""
		...

	def centerGraph(self) -> None:
		"""Transforming all positions such that the new center is at(0,0)."""
		...

	@overload
	def desiredEdgeLength(self) -> float:
		"""Returns the edge length array for all edges."""
		...

	@overload
	def desiredEdgeLength(self) -> float:
		"""Returns the edge length array for all edges."""
		...

	@overload
	def edgeInfo(self) -> EdgeAdjInfo:
		"""Returns theEdgeAdjInfoarray for all edges."""
		...

	@overload
	def edgeInfo(self) -> EdgeAdjInfo:
		"""Returns theEdgeAdjInfoarray for all edges."""
		...

	@overload
	def edgeInfo(self, i : int) -> EdgeAdjInfo:
		"""Returns the adjacency information for the edge at indexiinm_edgeAdj."""
		...

	@overload
	def edgeInfo(self, i : int) -> EdgeAdjInfo:
		"""Returns the adjacency information for the edge at indexiinm_edgeAdj."""
		...

	def firstEdgeAdjIndex(self, nodeIndex : int) -> int:
		"""Returns the index of the first pair of the node with indexnodeIndexinm_nodeAdj."""
		...

	def for_all_nodes(self, begin : int, end : int, func : Callable) -> None:
		"""Callsfuncon all nodes with indices frombegintoend."""
		...

	def nextEdgeAdjIndex(self, currEdgeAdjIndex : int, nodeIndex : int) -> int:
		"""Returns the index of the next pair ofcurrEdgeAdjIndexof the node with indexnodeIndex."""
		...

	@overload
	def nodeInfo(self) -> NodeAdjInfo:
		"""Returns theNodeAdjInfoarray for all nodes."""
		...

	@overload
	def nodeInfo(self) -> NodeAdjInfo:
		"""Returns theNodeAdjInfoarray for all nodes."""
		...

	@overload
	def nodeInfo(self, i : int) -> NodeAdjInfo:
		"""Returns the adjacency information for the node at indexiinm_nodeAdj."""
		...

	@overload
	def nodeInfo(self, i : int) -> NodeAdjInfo:
		"""Returns the adjacency information for the node at indexiinm_nodeAdj."""
		...

	def nodeMoveRadius(self) -> float:
		"""Returns the node movement radius array for all nodes."""
		...

	@overload
	def nodeSize(self) -> float:
		"""Returns the node size array for all nodes."""
		...

	@overload
	def nodeSize(self) -> float:
		"""Returns the node size array for all nodes."""
		...

	@overload
	def nodeXPos(self) -> float:
		"""Returns thexcoord array for all nodes."""
		...

	@overload
	def nodeXPos(self) -> float:
		"""Returns thexcoord array for all nodes."""
		...

	@overload
	def nodeYPos(self) -> float:
		"""Returns theycoord array for all nodes."""
		...

	@overload
	def nodeYPos(self) -> float:
		"""Returns theycoord array for all nodes."""
		...

	def numEdges(self) -> int:
		"""Returns the number of edges."""
		...

	def numNodes(self) -> int:
		"""Returns the number of nodes."""
		...

	@overload
	def readFrom(self, G : Graph, xPos : NodeArray[ CoordinateType ], yPos : NodeArray[ CoordinateType ], edgeLength : EdgeArray[ LengthType ], nodeSize : NodeArray[ SizeType ]) -> None:
		"""Updates anArrayGraphwith the given positions, edge lengths and node sizes and creates the edges."""
		...

	@overload
	def readFrom(self, GA : GraphAttributes, edgeLength : EdgeArray[ float ], nodeSize : NodeArray[ float ]) -> None:
		"""Updates anArrayGraphfromGraphAttributeswith the given edge lengths and node sizes and creates the edges."""
		...

	def transform(self, translate : float, scale : float) -> None:
		"""Transforms all positions via shifting them bytranslateand afterwards scaling byscale."""
		...

	def twinNodeIndex(self, currEdgeAdjIndex : int, nodeIndex : int) -> int:
		"""Returns the other node (notnodeIndex) of the pair with indexcurrEdgeAdjIndex."""
		...

	@overload
	def writeTo(self, G : Graph, xPos : NodeArray[ CoordinateType ], yPos : NodeArray[ CoordinateType ]) -> None:
		"""Store the data back toNodeArrayarrays with the given coordinate type."""
		...

	@overload
	def writeTo(self, GA : GraphAttributes) -> None:
		"""Store the data back inGraphAttributes."""
		...
