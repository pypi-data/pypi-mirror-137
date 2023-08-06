# file stubs/ogdf/HypergraphAttributesES.py generated from classogdf_1_1_hypergraph_attributes_e_s
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
class HypergraphAttributesES(ogdf.HypergraphAttributes):

	"""Stores additional attributes of edge standard representation of a hypergraph."""

	@overload
	def __init__(self) -> None:
		"""Initializes new instance of classHypergraphAttributes."""
		...

	@overload
	def __init__(self, pH : Hypergraph, pType : EdgeStandardType = EdgeStandardType.star) -> None:
		"""Initializes new instance of classHypergraphAttributes."""
		...

	def __destruct__(self) -> None:
		"""Destructor."""
		...

	def bends(self, e : edge) -> DPolyline:
		"""Returns the list of bend points of edgee."""
		...

	def boundingBox(self) -> DRect:
		"""Returns the bounding box of the hypergraph."""
		...

	def clearAllBends(self) -> None:
		...

	def height(self, v : node) -> float:
		"""Returns the height of a representation nodev."""
		...

	def removeUnnecessaryBendsHV(self) -> None:
		"""Removes unnecessary bend points in orthogonal segements."""
		...

	def repGA(self) -> GraphAttributes:
		...

	def repGraph(self) -> Graph:
		...

	@overload
	def setHeight(self, v : hypernode, pHeight : float) -> None:
		"""Sets the the height of hypernodev."""
		...

	@overload
	def setHeight(self, v : node, pHeight : float) -> None:
		"""Sets the the height of a representation nodev."""
		...

	@overload
	def setWidth(self, v : hypernode, pWidth : float) -> None:
		"""Sets the the width of hypernodev."""
		...

	@overload
	def setWidth(self, v : node, pWidth : float) -> None:
		"""Sets the the width of a representation nodev."""
		...

	@overload
	def setX(self, v : hypernode, pX : float) -> None:
		"""Sets the x-coordinate of hypernodev."""
		...

	@overload
	def setX(self, v : node, pX : float) -> None:
		"""Sets the x-coordinate of a representation nodev."""
		...

	@overload
	def setY(self, v : hypernode, pY : float) -> None:
		"""Sets the x-coordinate of hypernodev."""
		...

	@overload
	def setY(self, v : node, pY : float) -> None:
		"""Sets the y-coordinate of a representation nodev."""
		...

	@overload
	def type(self) -> EdgeStandardType:
		...

	@overload
	def type(self, v : hypernode) -> HypernodeElement.Type:
		"""Returns the type of representation nodev."""
		...

	@overload
	def type(self, v : node) -> HypernodeElement.Type:
		"""Returns the type of representation nodev."""
		...

	def width(self, v : node) -> float:
		"""Returns the width of a representation nodev."""
		...

	def x(self, v : node) -> float:
		"""Returns the x-coordinate of representation nodev."""
		...

	def y(self, v : node) -> float:
		"""Returns the y-coordinate of a representation nodev."""
		...
