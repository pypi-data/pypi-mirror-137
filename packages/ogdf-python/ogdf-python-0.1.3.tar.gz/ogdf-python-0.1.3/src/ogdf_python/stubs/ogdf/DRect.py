# file stubs/ogdf/DRect.py generated from classogdf_1_1_d_rect
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
class DRect(object):

	"""Rectangles with real coordinates."""

	#: The lower left point of the rectangle.
	m_p1 : DPoint = ...

	#: The upper right point of the rectangle.
	m_p2 : DPoint = ...

	@overload
	def __init__(self) -> None:
		"""Creates a rectangle with lower left and upper right point (0,0)."""
		...

	@overload
	def __init__(self, p1 : DPoint, p2 : DPoint) -> None:
		"""Creates a rectangle with lower left pointp1and upper right pointp2."""
		...

	@overload
	def __init__(self, dr : DRect) -> None:
		"""Copy constructor."""
		...

	@overload
	def __init__(self, dl : DSegment) -> None:
		"""Creates a rectangle defined by the end points of line segmentdl."""
		...

	@overload
	def __init__(self, x1 : float, y1 : float, x2 : float, y2 : float) -> None:
		"""Creates a rectangle with lower left point (x1,y1) and upper right point (x2,y2)."""
		...

	def __destruct__(self) -> None:
		...

	def bottom(self) -> DSegment:
		"""Returns the bottom side of the rectangle."""
		...

	def contains(self, p : DPoint) -> bool:
		"""Returns true iffplies within this rectangle, modulo the comparison epsilonOGDF_GEOM_ET."""
		...

	def height(self) -> float:
		"""Returns the height of the rectangle."""
		...

	def intersection(self, segment : DSegment) -> bool:
		"""Returns true iffsegmentintersects thisDRect."""
		...

	def left(self) -> DSegment:
		"""Returns the left side of the rectangle."""
		...

	def normalize(self) -> None:
		"""Normalizes the rectangle."""
		...

	def __ne__(self, dr : DRect) -> bool:
		"""Inequality operator."""
		...

	def __assign__(self, dr : DRect) -> DRect:
		"""Assignment operator."""
		...

	def __eq__(self, dr : DRect) -> bool:
		"""Equality operator: both rectangles have the same coordinates."""
		...

	def p1(self) -> DPoint:
		"""Returns the lower left point of the rectangle."""
		...

	def p2(self) -> DPoint:
		"""Returns the upper right point of the rectangle."""
		...

	def right(self) -> DSegment:
		"""Returns the right side of the rectangle."""
		...

	def top(self) -> DSegment:
		"""Returns the top side of the rectangle."""
		...

	def width(self) -> float:
		"""Returns the width of the rectangle."""
		...

	def xInvert(self) -> None:
		"""Swaps the x-coordinates of the two points."""
		...

	def yInvert(self) -> None:
		"""Swaps the y-coordinates of the two points."""
		...

	def parallelDist(self, d1 : DSegment, d2 : DSegment) -> float:
		"""Computes distance between parallel line segments."""
		...

	def pointDist(self, p1 : DPoint, p2 : DPoint) -> float:
		"""Computes distance between two points."""
		...
