# file stubs/ogdf/GenericSegment.py generated from classogdf_1_1_generic_segment
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
PointType = TypeVar('PointType')

class GenericSegment(ogdf.GenericLine[ PointType ], Generic[PointType]):

	"""Finite line segments."""

	@overload
	def __init__(self) -> None:
		"""Creates an empty line segment."""
		...

	@overload
	def __init__(self, dl : GenericLine[ PointType ]) -> None:
		"""Creates a line segment defined by the start and end point of linedl."""
		...

	@overload
	def __init__(self, ds : GenericSegment[ PointType ]) -> None:
		"""Copy constructor."""
		...

	@overload
	def __init__(self, p1 : PointType, p2 : PointType) -> None:
		"""Creates a line segment fromp1top2."""
		...

	@overload
	def __init__(self, x1 : float, y1 : float, x2 : float, y2 : float) -> None:
		"""Creates a line segment from (x1,y1) to (x2,y2)."""
		...

	def contains(self, p : PointType) -> bool:
		"""Returns true iffplies on this line segment."""
		...

	def dx(self) -> GenericLine[ PointType ].numberType:
		"""Returns the x-coordinate of the difference (end point - start point)."""
		...

	def dy(self) -> GenericLine[ PointType ].numberType:
		"""Returns the y-coordinate of the difference (end point - start point)."""
		...

	def end(self) -> PointType:
		"""Returns the end point of the line segment."""
		...

	def horIntersection(self, horAxis : float, crossing : float) -> IntersectionType:
		"""Computes the intersection of this line segment and the horizontal line through y =horAxis."""
		...

	def intersection(self, segment : GenericSegment[ PointType ], inter : PointType, endpoints : bool = True) -> IntersectionType:
		"""Returns an IntersectionType specifying whethersegmentand this line segment intersect."""
		...

	def length(self) -> float:
		"""Returns the length (Euclidean distance between start and end point) of this line segment."""
		...

	def __ne__(self, dl : GenericSegment[ PointType ]) -> bool:
		"""Inequality operator."""
		...

	def __assign__(self, ds : GenericSegment[ PointType ]) -> GenericSegment:
		"""Copy assignment operator."""
		...

	def __eq__(self, dl : GenericSegment[ PointType ]) -> bool:
		"""Equality operator."""
		...

	def start(self) -> PointType:
		"""Returns the start point of the line segment."""
		...

	def verIntersection(self, verAxis : float, crossing : float) -> IntersectionType:
		"""Computes the intersection between this line segment and the vertical line through x =verAxis."""
		...
