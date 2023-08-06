# file stubs/ogdf/GraphAttributes.py generated from classogdf_1_1_graph_attributes
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
Rectangle = TypeVar('Rectangle')

class GraphAttributes(object):

	"""Stores additional attributes of a graph (like layout information)."""

	# Flags for enabling attributes.

	#: Corresponds to node attributesx(node),y(node),width(node),height(node), andshape(node).
	nodeGraphics : int = ...

	#: Corresponds to edge attributebends(edge).
	edgeGraphics : int = ...

	#: Corresponds to edge attributeintWeight(edge).
	edgeIntWeight : int = ...

	#: Corresponds to edge attributedoubleWeight(edge).
	edgeDoubleWeight : int = ...

	#: Corresponds to edge attributelabel(edge).
	edgeLabel : int = ...

	#: Corresponds to node attributelabel(node).
	nodeLabel : int = ...

	#: Corresponds to edge attributetype(edge).
	edgeType : int = ...

	#: Corresponds to node attributetype(node).
	nodeType : int = ...

	#: Corresponds to node attributeidNode(node).
	nodeId : int = ...

	#: Corresponds to edge attributearrowType(edge).
	edgeArrow : int = ...

	#: Corresponds to edge attributesstrokeColor(edge),strokeType(edge), andstrokeWidth(edge).
	edgeStyle : int = ...

	#: Corresponds to node attributesstrokeColor(node),strokeType(node),strokeWidth(node),fillPattern(node),fillColor(node), andfillBgColor(node).
	nodeStyle : int = ...

	#: Corresponds to node attributetemplateNode(node).
	nodeTemplate : int = ...

	#: Corresponds to edge attributes modified byaddSubGraph(edge, int),inSubGraph(edge, int) const, andremoveSubGraph(edge, int).
	edgeSubGraphs : int = ...

	#: Corresponds to node attributeweight(node).
	nodeWeight : int = ...

	#: Corresponds to node attributez(node). Note that all methods work on 2D coordinates only.
	threeD : int = ...

	#: Corresponds to node attributesxLabel(node),yLabel(node), andzLabel(node).
	nodeLabelPosition : int = ...

	#: Enables all available flags.
	all : int = ...

	# Construction and management of attributes

	@overload
	def __init__(self) -> None:
		"""Constructs graph attributes for no associated graph (default constructor)."""
		...

	@overload
	def __init__(self, G : Graph, attr : int = nodeGraphics|edgeGraphics) -> None:
		"""Constructs graph attributes associated with the graphG."""
		...

	@overload
	def __init__(self, _ : GraphAttributes) -> None:
		"""Copy constructor."""
		...

	def __assign__(self, _ : GraphAttributes) -> GraphAttributes:
		"""Copy assignment operator."""
		...

	def __destruct__(self) -> None:
		...

	def attributes(self) -> int:
		"""Returns currently accessible attributes."""
		...

	def has(self, attr : int) -> bool:
		"""Returns true iff all attributes inattrare available."""
		...

	@overload
	def init(self, G : Graph, attr : int) -> None:
		"""Initializes the graph attributes for graphG."""
		...

	@overload
	def init(self, attr : int) -> None:
		"""Re-initializes the graph attributes while maintaining the associated graph."""
		...

	def addAttributes(self, attr : int) -> None:
		"""Enables attributes specified byattrand allocates required memory."""
		...

	def destroyAttributes(self, attr : int) -> None:
		"""Disables attributes specified byattrand releases available memory."""
		...

	def constGraph(self) -> Graph:
		"""Returns a reference to the associated graph."""
		...

	# General attributes

	@overload
	def directed(self) -> bool:
		"""Returns if the graph is directed."""
		...

	@overload
	def directed(self) -> bool:
		"""Returns if the graph is directed."""
		...

	# Node attributes

	@overload
	def x(self, v : node) -> float:
		"""Returns the x-coordinate of nodev."""
		...

	@overload
	def x(self, v : node) -> float:
		"""Returns the x-coordinate of nodev."""
		...

	@overload
	def y(self, v : node) -> float:
		"""Returns the y-coordinate of nodev."""
		...

	@overload
	def y(self, v : node) -> float:
		"""Returns the y-coordinate of nodev."""
		...

	@overload
	def z(self, v : node) -> float:
		"""Returns the z-coordinate of nodev."""
		...

	@overload
	def z(self, v : node) -> float:
		"""Returns the z-coordinate of nodev."""
		...

	@overload
	def xLabel(self, v : node) -> float:
		"""Returns the label x-coordinate of nodev."""
		...

	@overload
	def xLabel(self, v : node) -> float:
		"""Returns the label x-coordinate of nodev."""
		...

	@overload
	def yLabel(self, v : node) -> float:
		"""Returns the label y-coordinate of nodev."""
		...

	@overload
	def yLabel(self, v : node) -> float:
		"""Returns the label y-coordinate of nodev."""
		...

	@overload
	def zLabel(self, v : node) -> float:
		"""Returns the label z-coordinate of nodev."""
		...

	@overload
	def zLabel(self, v : node) -> float:
		"""Returns the label z-coordinate of nodev."""
		...

	@overload
	def width(self, v : node) -> float:
		"""Returns the width of the bounding box of nodev."""
		...

	@overload
	def width(self, v : node) -> float:
		"""Returns the width of the bounding box of nodev."""
		...

	@overload
	def width(self) -> NodeArray[ float ]:
		"""Returns a reference to the node arraym_width."""
		...

	@overload
	def width(self) -> NodeArray[ float ]:
		"""Returns a reference to the node array #m_width."""
		...

	@overload
	def height(self, v : node) -> float:
		"""Returns the height of the bounding box of nodev."""
		...

	@overload
	def height(self, v : node) -> float:
		"""Returns the height of the bounding box of nodev."""
		...

	@overload
	def height(self) -> NodeArray[ float ]:
		"""Returns a reference to the node arraym_height."""
		...

	@overload
	def height(self) -> NodeArray[ float ]:
		"""Returns a reference to the node arraym_height."""
		...

	@overload
	def shape(self, v : node) -> Shape:
		"""Returns the shape type of nodev."""
		...

	@overload
	def shape(self, v : node) -> Shape:
		"""Returns the shape type of nodev."""
		...

	@overload
	def strokeType(self, v : node) -> StrokeType:
		"""Returns the stroke type of nodev."""
		...

	@overload
	def strokeType(self, v : node) -> StrokeType:
		"""Returns the stroke type of nodev."""
		...

	@overload
	def strokeColor(self, v : node) -> Color:
		"""Returns the stroke color of nodev."""
		...

	@overload
	def strokeColor(self, v : node) -> Color:
		"""Returns the stroke color of nodev."""
		...

	@overload
	def strokeWidth(self, v : node) -> float:
		"""Returns the stroke width of nodev."""
		...

	@overload
	def strokeWidth(self, v : node) -> float:
		"""Returns the stroke width of nodev."""
		...

	@overload
	def fillPattern(self, v : node) -> FillPattern:
		"""Returns the fill pattern of nodev."""
		...

	@overload
	def fillPattern(self, v : node) -> FillPattern:
		"""Returns the fill pattern of nodev."""
		...

	@overload
	def fillColor(self, v : node) -> Color:
		"""Returns the fill color of nodev."""
		...

	@overload
	def fillColor(self, v : node) -> Color:
		"""Returns the fill color of nodev."""
		...

	@overload
	def fillBgColor(self, v : node) -> Color:
		"""Returns the background color of fill patterns for nodev."""
		...

	@overload
	def fillBgColor(self, v : node) -> Color:
		"""Returns the background color of fill patterns for nodev."""
		...

	@overload
	def label(self, v : node) -> str:
		"""Returns the label of nodev."""
		...

	@overload
	def label(self, v : node) -> str:
		"""Returns the label of nodev."""
		...

	@overload
	def templateNode(self, v : node) -> str:
		"""Returns the template name of nodev."""
		...

	@overload
	def templateNode(self, v : node) -> str:
		"""Returns the template name of nodev."""
		...

	@overload
	def weight(self, v : node) -> int:
		"""Returns the weight of nodev."""
		...

	@overload
	def weight(self, v : node) -> int:
		"""Returns the weight of nodev."""
		...

	@overload
	def type(self, v : node) -> Graph.NodeType:
		"""Returns the type of nodev."""
		...

	@overload
	def type(self, v : node) -> Graph.NodeType:
		"""Returns the type of nodev."""
		...

	@overload
	def idNode(self, v : node) -> int:
		"""Returns the user ID of nodev."""
		...

	@overload
	def idNode(self, v : node) -> int:
		"""Returns the user ID of nodev."""
		...

	# Edge attributes

	@overload
	def bends(self, e : edge) -> DPolyline:
		"""Returns the list of bend points of edgee."""
		...

	@overload
	def bends(self, e : edge) -> DPolyline:
		"""Returns the list of bend points of edgee."""
		...

	@overload
	def arrowType(self, e : edge) -> EdgeArrow:
		"""Returns the arrow type of edgee."""
		...

	@overload
	def arrowType(self, e : edge) -> EdgeArrow:
		"""Returns the arrow type of edgee."""
		...

	@overload
	def strokeType(self, e : edge) -> StrokeType:
		"""Returns the stroke type of edgee."""
		...

	@overload
	def strokeType(self, e : edge) -> StrokeType:
		"""Returns the stroke type of edgee."""
		...

	@overload
	def strokeColor(self, e : edge) -> Color:
		"""Returns the stroke color of edgee."""
		...

	@overload
	def strokeColor(self, e : edge) -> Color:
		"""Returns the stroke color of edgee."""
		...

	@overload
	def strokeWidth(self, e : edge) -> float:
		"""Returns the stroke width of edgee."""
		...

	@overload
	def strokeWidth(self, e : edge) -> float:
		"""Returns the stroke width of edgee."""
		...

	@overload
	def label(self, e : edge) -> str:
		"""Returns the label of edgee."""
		...

	@overload
	def label(self, e : edge) -> str:
		"""Returns the label of edgee."""
		...

	@overload
	def intWeight(self, e : edge) -> int:
		"""Returns the (integer) weight of edgee."""
		...

	@overload
	def intWeight(self, e : edge) -> int:
		"""Returns the (integer) weight of edgee."""
		...

	@overload
	def doubleWeight(self, e : edge) -> float:
		"""Returns the (real number) weight of edgee."""
		...

	@overload
	def doubleWeight(self, e : edge) -> float:
		"""Returns the (real number) weight of edgee."""
		...

	@overload
	def type(self, e : edge) -> Graph.EdgeType:
		"""Returns the type of edgee."""
		...

	@overload
	def type(self, e : edge) -> Graph.EdgeType:
		"""Returns the type of edgee."""
		...

	@overload
	def subGraphBits(self, e : edge) -> int:
		"""Returns the edgesubgraph value of an edgee."""
		...

	@overload
	def subGraphBits(self, e : edge) -> int:
		"""Returns the edgesubgraph value of an edgee."""
		...

	def inSubGraph(self, e : edge, n : int) -> bool:
		"""Checks whether edgeebelongs to basic graphn."""
		...

	def addSubGraph(self, e : edge, n : int) -> None:
		"""Adds edgeeto basic graphn."""
		...

	def removeSubGraph(self, e : edge, n : int) -> None:
		"""Removes edgeefrom basic graphn."""
		...

	# Layout transformations

	@overload
	def scale(self, sx : float, sy : float, scaleNodes : bool = True) -> None:
		"""Scales the layout by (sx,sy)."""
		...

	@overload
	def scale(self, s : float, scaleNodes : bool = True) -> None:
		"""Scales the layout bys."""
		...

	def translate(self, dx : float, dy : float) -> None:
		"""Translates the layout by (dx,dy)."""
		...

	def translateToNonNeg(self) -> None:
		"""Translates the layout such that the lower left corner is at (0,0)."""
		...

	@overload
	def flipVertical(self) -> None:
		"""Flips the layout vertically within its bounding box."""
		...

	@overload
	def flipVertical(self, box : DRect) -> None:
		"""Flips the (whole) layout vertically such that the part inboxremains in this area."""
		...

	@overload
	def flipHorizontal(self) -> None:
		"""Flips the layout horizontally within its bounding box."""
		...

	@overload
	def flipHorizontal(self, box : DRect) -> None:
		"""Flips the (whole) layout horizontally such that the part inboxremains in this area."""
		...

	@overload
	def scaleAndTranslate(self, sx : float, sy : float, dx : float, dy : float, scaleNodes : bool = True) -> None:
		"""Scales the layout by (sx,sy) and then translates it by (dx,dy)."""
		...

	@overload
	def scaleAndTranslate(self, s : float, dx : float, dy : float, scaleNodes : bool = True) -> None:
		"""Scales the layout bysand then translates it by (dx,dy)."""
		...

	def rotateRight90(self) -> None:
		"""Rotates the layout by 90 degree (in clockwise direction) around the origin."""
		...

	def rotateLeft90(self) -> None:
		"""Rotates the layout by 90 degree (in counter-clockwise direction) around the origin."""
		...

	# Utility functions

	def point(self, v : node) -> DPoint:
		"""Returns a DPoint corresponding to the x- and y-coordinates ofv."""
		...

	def transferToOriginal(self, origAttr : GraphAttributes) -> None:
		"""Copies attributes of this toorigAttr."""
		...

	def transferToCopy(self, copyAttr : GraphAttributes) -> None:
		"""Copies attributes of this tocopyAttr."""
		...

	def boundingBox(self) -> DRect:
		"""Returns the bounding box of the graph."""
		...

	def nodeBoundingBoxes(self, boundingBoxes : NodeArray[ Rectangle ]) -> None:
		"""Computes the bounding rectangle for each node."""
		...

	def setAllWidth(self, w : float) -> None:
		"""Sets the width of all nodes tow."""
		...

	def setAllHeight(self, h : float) -> None:
		"""Sets the height of all nodes toh."""
		...

	def clearAllBends(self) -> None:
		"""Removes all edge bends."""
		...

	def removeUnnecessaryBendsHV(self) -> None:
		"""Removes unnecessary bend points in orthogonal segements."""
		...

	def addNodeCenter2Bends(self, mode : int = 1) -> None:
		"""Adds additional bend points to all edges for connecting their endpoints."""
		...

	def isAssociationClass(self, v : node) -> bool:
		"""Returns true iffvrepresents an association class."""
		...

	@overload
	def hierarchyList(self, list : List[List[node]  ]) -> int:
		"""Returns a list of all inheritance hierarchies in the graph."""
		...

	@overload
	def hierarchyList(self, list : List[List[edge]  ]) -> int:
		"""Returns a list of all inheritance hierarchies in the graph."""
		...

	#: bit vector of currently used attributes
	m_attributes : int = ...

	#: list of bend points of an edge
	m_bends : EdgeArray[DPolyline] = ...

	#: whether or not the graph is directed
	m_directed : bool = ...

	#: (real number) weight of an edge
	m_doubleWeight : EdgeArray[ float ] = ...

	#: arrow type of an edge
	m_edgeArrow : EdgeArray[EdgeArrow] = ...

	#: label of an edge
	m_edgeLabel : EdgeArray[ str ] = ...

	#: stroke of an edge
	m_edgeStroke : EdgeArray[Stroke] = ...

	#: type of an edge (association or generalization)
	m_eType : EdgeArray[Graph.EdgeType] = ...

	#: height of a nodes's bounding box
	m_height : NodeArray[ float ] = ...

	#: (integer) weight of an edge
	m_intWeight : EdgeArray[  int ] = ...

	#: fill of a node
	m_nodeFill : NodeArray[Fill] = ...

	#: user ID of a node
	m_nodeId : NodeArray[  int ] = ...

	#: (integer) weight of a node
	m_nodeIntWeight : NodeArray[  int ] = ...

	#: label of a node
	m_nodeLabel : NodeArray[ str ] = ...

	#: x-coordinate of a node label
	m_nodeLabelPosX : NodeArray[ float ] = ...

	#: y-coordinate of a node label
	m_nodeLabelPosY : NodeArray[ float ] = ...

	#: z-coordinate of a node label
	m_nodeLabelPosZ : NodeArray[ float ] = ...

	#: shape of a node
	m_nodeShape : NodeArray[Shape] = ...

	#: stroke of a node
	m_nodeStroke : NodeArray[Stroke] = ...

	#: name of template of a node
	m_nodeTemplate : NodeArray[ str ] = ...

	#: associated graph
	m_pGraph : Graph = ...

	#: is element of subgraphs given by bitvector
	m_subGraph : EdgeArray[  int ] = ...

	#: type (vertex, dummy, generalizationMerger)
	m_vType : NodeArray[Graph.NodeType] = ...

	#: width of a node's bounding box
	m_width : NodeArray[ float ] = ...

	#: x-coordinate of a node
	m_x : NodeArray[ float ] = ...

	#: y-coordinate of a node
	m_y : NodeArray[ float ] = ...

	#: z-coordinate of a node
	m_z : NodeArray[ float ] = ...
