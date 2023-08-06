# file stubs/ogdf/GenericLine.py generated from classogdf_1_1_generic_line
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
PointType = TypeVar('PointType')

class GenericLine(Generic[PointType]):

	"""Infinite lines."""

	numberType : Type = PointType.numberType

	#: The first point of the line.
	m_p1 : PointType = ...

	#: The second point of the line.
	m_p2 : PointType = ...

	def dx(self) -> numberType:
		"""Returns the x-coordinate of the difference (second point - first point)."""
		...

	def dy(self) -> numberType:
		"""Returns the y-coordinate of the difference (second point - first point)."""
		...

	@overload
	def __init__(self) -> None:
		"""Creates an empty line."""
		...

	@overload
	def __init__(self, dl : GenericLine[ PointType ]) -> None:
		"""Copy constructor."""
		...

	@overload
	def __init__(self, p1 : PointType, p2 : PointType) -> None:
		"""Creates a line through the pointsp1andp2."""
		...

	@overload
	def __init__(self, x1 : numberType, y1 : numberType, x2 : numberType, y2 : numberType) -> None:
		"""Creates a line through the points (x1,y1) and (x2,y2)."""
		...

	def contains(self, p : DPoint) -> bool:
		"""Returns true iffplies on this line."""
		...

	def det(self, line : GenericLine[ PointType ]) -> float:
		"""Determines iflineis left or right of this line."""
		...

	def horIntersection(self, horAxis : float, crossing : float) -> IntersectionType:
		"""Computes the intersection of this line and the horizontal line through y =horAxis."""
		...

	def intersection(self, line : GenericLine[ PointType ], inter : DPoint) -> IntersectionType:
		"""Returns an IntersectionType specifying whetherlineand this line intersect."""
		...

	def isHorizontal(self) -> bool:
		"""Returns true iff this line runs horizontally."""
		...

	def isVertical(self) -> bool:
		"""Returns true iff this line runs vertically."""
		...

	def __ne__(self, dl : GenericLine[ PointType ]) -> bool:
		"""Inequality operator."""
		...

	def __assign__(self, dl : GenericLine[ PointType ]) -> GenericLine[ PointType ]:
		"""Assignment operator."""
		...

	def __eq__(self, dl : GenericLine[ PointType ]) -> bool:
		"""Equality operator."""
		...

	def slope(self) -> float:
		"""Returns the slope of the line."""
		...

	def verIntersection(self, verAxis : float, crossing : float) -> IntersectionType:
		"""Computes the intersection between this line and the vertical line through x =verAxis."""
		...

	def yAbs(self) -> float:
		"""Returns the value y' such that (0,y') lies on the unlimited straight-line defined by this line."""
		...
