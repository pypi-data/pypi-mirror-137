# file stubs/ogdf/ClusterGraphAttributes.py generated from classogdf_1_1_cluster_graph_attributes
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
class ClusterGraphAttributes(ogdf.GraphAttributes):

	"""Stores additional attributes of a clustered graph (like layout information)."""

	# Flags for enabling attributes

	#: Corresponds to cluster attributesx(cluster),y(cluster),width(cluster),height(cluster).
	clusterGraphics : int = ...

	#: Corresponds to cluster attributesstrokeColor(cluster),strokeType(cluster),strokeWidth(cluster),fillPattern(cluster),fillColor(cluster), andfillBgColor(cluster).
	clusterStyle : int = ...

	#: Corresponds to cluster attributelabel(cluster).
	clusterLabel : int = ...

	#: Corresponds to cluster attributetemplateCluster(cluster).
	clusterTemplate : int = ...

	#: Enables all available flags.
	all : int = ...

	# Construction and management of attributes

	@overload
	def __init__(self) -> None:
		"""Constructs cluster graph attributes for no associated graph."""
		...

	@overload
	def __init__(self, cg : ClusterGraph, initAttributes : int = nodeGraphics|edgeGraphics|clusterGraphics) -> None:
		"""Constructs cluster graph attributes for cluster graphcgwith attributesinitAttributes."""
		...

	def __destruct__(self) -> None:
		...

	@overload
	def init(self, cg : ClusterGraph, attr : int = 0) -> None:
		"""Initializes theClusterGraphAttributesforClusterGraphcg."""
		...

	@overload
	def init(self, attr : int = 0) -> None:
		"""Re-initializes theClusterGraphAttributeswhile maintaining the associated CluterGraph."""
		...

	def addAttributes(self, attr : int) -> None:
		"""Enables attributes specified byattrand allocates required memory."""
		...

	def destroyAttributes(self, attr : int) -> None:
		"""Disables attributes specified byattrand releases available memory."""
		...

	def constClusterGraph(self) -> ClusterGraph:
		"""Returns the associated cluster graph."""
		...

	# Cluster attributes

	@overload
	def x(self, c : cluster) -> float:
		"""Returns the x-position of clusterc'scage (lower left corner)."""
		...

	@overload
	def x(self, c : cluster) -> float:
		"""Returns the x-position of clusterc'scage (lower left corner)."""
		...

	@overload
	def y(self, c : cluster) -> float:
		"""Returns the y-position of clusterc'scage (lower left corner)."""
		...

	@overload
	def y(self, c : cluster) -> float:
		"""Returns the y-position of clusterc'scage (lower left corner)."""
		...

	@overload
	def width(self, c : cluster) -> float:
		"""Returns the width of clusterc."""
		...

	@overload
	def width(self, c : cluster) -> float:
		"""Returns the width of clusterc."""
		...

	@overload
	def height(self, c : cluster) -> float:
		"""Returns the height of clusterc."""
		...

	@overload
	def height(self, c : cluster) -> float:
		"""Returns the height of clusterc."""
		...

	@overload
	def strokeType(self, c : cluster) -> StrokeType:
		"""Returns the stroke type of clusterc."""
		...

	@overload
	def strokeType(self, c : cluster) -> StrokeType:
		"""Returns the stroke type of clusterc."""
		...

	@overload
	def strokeColor(self, c : cluster) -> Color:
		"""Returns the stroke color of clusterc."""
		...

	@overload
	def strokeColor(self, c : cluster) -> Color:
		"""Returns the stroke color of clusterc."""
		...

	@overload
	def strokeWidth(self, c : cluster) -> float:
		"""Returns the stroke width of clusterc."""
		...

	@overload
	def strokeWidth(self, c : cluster) -> float:
		"""Returns the stroke width of clusterc."""
		...

	@overload
	def fillPattern(self, c : cluster) -> FillPattern:
		"""Returns the fill pattern of clusterc."""
		...

	@overload
	def fillPattern(self, c : cluster) -> FillPattern:
		"""Returns the fill pattern of clusterc."""
		...

	@overload
	def fillColor(self, c : cluster) -> Color:
		"""Returns the fill color of clusterc."""
		...

	@overload
	def fillColor(self, c : cluster) -> Color:
		"""Returns the fill color of clusterc."""
		...

	@overload
	def fillBgColor(self, c : cluster) -> Color:
		"""Returns the background color of fill patterns for clusterc."""
		...

	@overload
	def fillBgColor(self, c : cluster) -> Color:
		"""Returns the background color of fill patterns for clusterc."""
		...

	@overload
	def label(self, c : cluster) -> str:
		"""Returns the label of clusterc."""
		...

	@overload
	def label(self, c : cluster) -> str:
		"""Returns the label of clusterc."""
		...

	@overload
	def templateCluster(self, c : cluster) -> str:
		"""Returns the template of clusterc."""
		...

	@overload
	def templateCluster(self, c : cluster) -> str:
		"""Returns the template of clusterc."""
		...

	@overload
	def scale(self, sx : float, sy : float, scaleNodes : bool = True) -> None:
		"""Scales the layout by (sx,sy)."""
		...

	def translate(self, dx : float, dy : float) -> None:
		"""Translates the layout by (dx,dy)."""
		...

	@overload
	def flipVertical(self, box : DRect) -> None:
		"""Flips the (whole) layout vertically such that the part inboxremains in this area."""
		...

	@overload
	def flipHorizontal(self, box : DRect) -> None:
		"""Flips the (whole) layout horizontally such that the part inboxremains in this area."""
		...

	@overload
	def scale(self, sx : float, sy : float, scaleNodes : bool = True) -> None:
		...

	@overload
	def scale(self, s : float, scaleNodes : bool = True) -> None:
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

	# Utility functions

	def boundingBox(self) -> DRect:
		"""Returns the bounding box of the layout."""
		...

	def updateClusterPositions(self, boundaryDist : float = 1.0) -> None:
		"""Updates positions of cluster boundaries wrt to children and child clusters."""
		...

	def clusterOf(self, v : node) -> cluster:
		"""Returns the parent cluster of nodev."""
		...

	#: Name of cluster template.
	m_clusterTemplate : ClusterArray[ str ] = ...

	#: Fill(style of interior)
	m_fill : ClusterArray[Fill] = ...

	#: Cluster height.
	m_height : ClusterArray[ float ] = ...

	#: Cluster label.
	m_label : ClusterArray[ str ] = ...

	#: Only points to existing graphs.
	m_pClusterGraph : ClusterGraph = ...

	#: Stroke(style of boundary)
	m_stroke : ClusterArray[Stroke] = ...

	#: Cluster width.
	m_width : ClusterArray[ float ] = ...

	#: X-position of lower left corner.
	m_x : ClusterArray[ float ] = ...

	#: Y-position of lower left corner.
	m_y : ClusterArray[ float ] = ...

	@overload
	def fillBgColor(self, v : node) -> Color:
		"""Returns the background color of fill patterns for nodev."""
		...

	@overload
	def fillBgColor(self, v : node) -> Color:
		"""Returns the background color of fill patterns for nodev."""
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
	def fillPattern(self, v : node) -> FillPattern:
		"""Returns the fill pattern of nodev."""
		...

	@overload
	def fillPattern(self, v : node) -> FillPattern:
		"""Returns the fill pattern of nodev."""
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
	def height(self, v : node) -> float:
		"""Returns the height of the bounding box of nodev."""
		...

	@overload
	def height(self, v : node) -> float:
		"""Returns the height of the bounding box of nodev."""
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
	def label(self, v : node) -> str:
		"""Returns the label of nodev."""
		...

	@overload
	def label(self, v : node) -> str:
		"""Returns the label of nodev."""
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
	def strokeColor(self, v : node) -> Color:
		"""Returns the stroke color of nodev."""
		...

	@overload
	def strokeColor(self, v : node) -> Color:
		"""Returns the stroke color of nodev."""
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
	def strokeType(self, v : node) -> StrokeType:
		"""Returns the stroke type of nodev."""
		...

	@overload
	def strokeType(self, v : node) -> StrokeType:
		"""Returns the stroke type of nodev."""
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
	def strokeWidth(self, v : node) -> float:
		"""Returns the stroke width of nodev."""
		...

	@overload
	def strokeWidth(self, v : node) -> float:
		"""Returns the stroke width of nodev."""
		...

	@overload
	def width(self) -> NodeArray[ float ]:
		"""Returns a reference to the node array #m_width."""
		...

	@overload
	def width(self) -> NodeArray[ float ]:
		"""Returns a reference to the node arraym_width."""
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
