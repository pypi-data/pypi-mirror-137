# file stubs/ogdf/HypergraphAttributes.py generated from classogdf_1_1_hypergraph_attributes
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
class HypergraphAttributes(object):

	"""Stores additional attributes of a hypergraph."""

	#: Height of a hypernodes bounding box.
	m_height : HypernodeArray[ float ] = ...

	#: Only points to an existing hypergraph.
	m_hypergraph : Hypergraph = ...

	#: Label of a hypernode.
	m_label : HypernodeArray[ str ] = ...

	#: Shape of a hypernode.
	m_shape : HypernodeArray[  int ] = ...

	#: Width of a hypernode bounding box.
	m_width : HypernodeArray[ float ] = ...

	#: Coordinate x of a hypernod.e.
	m_x : HypernodeArray[ float ] = ...

	#: Coordinate y of a hypernode.
	m_y : HypernodeArray[ float ] = ...

	@overload
	def __init__(self) -> None:
		"""Initializes new instance of classHypergraphAttributes."""
		...

	@overload
	def __init__(self, H : Hypergraph) -> None:
		"""Initializes new instance of classHypergraphAttributes."""
		...

	def __destruct__(self) -> None:
		"""Destructor."""
		...

	def constHypergraph(self) -> Hypergraph:
		...

	def height(self, v : hypernode) -> float:
		"""Returns the height of the bounding box of hypernodev."""
		...

	def label(self, v : hypernode) -> str:
		"""Returns the label of hypernodev."""
		...

	def setHeight(self, v : hypernode, pHeight : int) -> None:
		"""Sets the the height of hypernodev."""
		...

	def setWidth(self, v : hypernode, pWidth : int) -> None:
		"""Sets the the width of hypernodev."""
		...

	def setX(self, v : hypernode, pX : float) -> None:
		"""Sets the x-coordinate of hypernodev."""
		...

	def setY(self, v : hypernode, pY : float) -> None:
		"""Sets the y-coordinate of hypernodev."""
		...

	def shape(self, v : hypernode) -> int:
		"""Returns the shape of hypernodev."""
		...

	def width(self, v : hypernode) -> float:
		"""Returns the width of the bounding box of hypernodev."""
		...

	def x(self, v : hypernode) -> float:
		"""Returns the x-coordinate of hypernodev."""
		...

	def y(self, v : hypernode) -> float:
		"""Returns the y-coordinate of hypernodev."""
		...
