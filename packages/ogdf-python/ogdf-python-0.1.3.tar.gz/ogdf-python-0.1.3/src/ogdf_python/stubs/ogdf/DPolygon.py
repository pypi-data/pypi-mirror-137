# file stubs/ogdf/DPolygon.py generated from classogdf_1_1_d_polygon
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
class DPolygon(ogdf.GenericPolyline[ DPoint ]):

	"""Polygons with real coordinates."""

	#: If true points are given in conter-clockwise order.
	m_counterclock : bool = ...

	@overload
	def __init__(self, cc : bool = True) -> None:
		"""Creates an empty polygon."""
		...

	@overload
	def __init__(self, dop : DPolygon) -> None:
		"""Copy constructor."""
		...

	@overload
	def __init__(self, rect : DRect, cc : bool = True) -> None:
		"""Creates a polgon from a rectangle."""
		...

	def containsPoint(self, p : DPoint) -> bool:
		"""Checks wether a Point /a p is inside the Poylgon or not."""
		...

	def counterclock(self) -> bool:
		"""Returns true iff points are given in counter-clockwise order."""
		...

	def getCrossPoints(self, p : DPolygon, crossPoints : List[DPoint]) -> int:
		"""Returns the list of intersection points of this polygon withp."""
		...

	def insertCrossPoint(self, p : DPoint) -> None:
		"""Inserts point p on every segment (a,b) withpin the open range ]a, b[."""
		...

	@overload
	def insertPoint(self, p : DPoint) -> ListIterator[DPoint]:
		"""Inserts pointp, that must lie on a polygon segment."""
		...

	@overload
	def insertPoint(self, p : DPoint, p1 : ListIterator[DPoint], p2 : ListIterator[DPoint]) -> ListIterator[DPoint]:
		"""Inserts pointp, but just searching from pointp1top2."""
		...

	def normalize(self) -> None:
		"""Deletes all points, which are not facets."""
		...

	@overload
	def __assign__(self, dop : DPolygon) -> DPolygon:
		"""Assignment operator."""
		...

	@overload
	def __assign__(self, rect : DRect) -> DPolygon:
		"""Assignment operator (for assigning from a rectangle)."""
		...

	def segment(self, it : ListConstIterator[DPoint]) -> DSegment:
		"""Returns the line segment that starts at positionit."""
		...

	def unify(self) -> None:
		"""Deletes all consecutive points that are equal."""
		...
