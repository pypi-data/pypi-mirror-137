# file stubs/ogdf/DIntersectableRect.py generated from classogdf_1_1_d_intersectable_rect
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
class DIntersectableRect(ogdf.DRect):

	"""Rectangles with real coordinates."""

	@overload
	def __init__(self) -> None:
		"""Creates a rectangle with lower left and upper right point (0,0)."""
		...

	@overload
	def __init__(self, dr : DIntersectableRect) -> None:
		"""Copy constructor."""
		...

	@overload
	def __init__(self, center : DPoint, width : float, height : float) -> None:
		"""Constructs a rectangle from thecenterpoint,widthandheight."""
		...

	@overload
	def __init__(self, p1 : DPoint, p2 : DPoint) -> None:
		"""Creates a rectangle with lower left pointp1and upper right pointp2."""
		...

	@overload
	def __init__(self, x1 : float, y1 : float, x2 : float, y2 : float) -> None:
		"""Creates a rectangle with lower left point (x1,y1) and upper right point (x1,y2)."""
		...

	def area(self) -> float:
		"""Area of the rectangle."""
		...

	def center(self) -> DPoint:
		"""Center of the rectangle."""
		...

	def distance(self, other : DIntersectableRect) -> float:
		"""Computes distance between two rectangles."""
		...

	def intersection(self, other : DIntersectableRect) -> DIntersectableRect:
		"""Returns the rectangle resulting from intersection of this andother. Returns a rectangle with zero width and height and center (0,0) if intersection is empty."""
		...

	def intersects(self, rectangle : DIntersectableRect) -> bool:
		"""Tests if this and the argumentrectangleintersect."""
		...

	def move(self, point : DPoint) -> None:
		"""Moves the rectangle such that its center is at the givenpoint."""
		...

	def __assign__(self, dr : DIntersectableRect) -> DIntersectableRect:
		"""Assignment operator."""
		...
