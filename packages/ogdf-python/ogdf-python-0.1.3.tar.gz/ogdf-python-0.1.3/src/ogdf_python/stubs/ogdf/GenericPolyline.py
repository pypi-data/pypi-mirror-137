# file stubs/ogdf/GenericPolyline.py generated from classogdf_1_1_generic_polyline
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
PointType = TypeVar('PointType')

class GenericPolyline(ogdf.List[ PointType ], Generic[PointType]):

	"""Polylines withPointTypepoints."""

	@overload
	def __init__(self) -> None:
		"""Creates an empty polyline."""
		...

	@overload
	def __init__(self, pl : GenericPolyline[ PointType ]) -> None:
		"""Copy constructor."""
		...

	@overload
	def __init__(self, pl : List[ PointType ]) -> None:
		"""Creates a polyline using the list of pointspl."""
		...

	def length(self) -> float:
		"""Returns the Euclidean length of the polyline."""
		...

	@overload
	def normalize(self, minAngle : float = Math.pi) -> None:
		"""Deletes all redundant points on the polyline that lie on a (nearly) straight line given by their adjacent points."""
		...

	@overload
	def normalize(self, src : PointType, tgt : PointType, minAngle : float = Math.pi) -> None:
		"""Deletes all redundant points on the polyline that lie on a (nearly) straight line given by their adjacent points."""
		...

	def __assign__(self, pl : GenericPolyline) -> GenericPolyline[ PointType ]:
		"""Assignment operator."""
		...

	def position(self, fraction : float, len : float = -1.0) -> DPoint:
		"""Returns a point on the polyline which isfraction*lenaway from the start point."""
		...

	def unify(self) -> None:
		"""Deletes all successive points with equal coordinates."""
		...

	def normalizeUnified(self, minAngle : float) -> None:
		"""Deletes all redundant points on the polyline that lie on a (nearly) straight line given by their adjacent points."""
		...
