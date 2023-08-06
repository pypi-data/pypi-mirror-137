# file stubs/ogdf/Layout.py generated from classogdf_1_1_layout
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
class Layout(object):

	"""Stores a layout of a graph (coordinates of nodes, bend points of edges)."""

	@overload
	def __init__(self) -> None:
		"""Creates a layout associated with no graph."""
		...

	@overload
	def __init__(self, G : Graph) -> None:
		"""Creates a layout associated with graphG."""
		...

	@overload
	def x(self) -> NodeArray[ float ]:
		"""Returns a reference to the array storing x-coordinates of nodes."""
		...

	@overload
	def x(self) -> NodeArray[ float ]:
		"""Returns a reference to the array storing x-coordinates of nodes."""
		...

	@overload
	def y(self) -> NodeArray[ float ]:
		"""Returns a reference to the array storing y-coordinates of nodes."""
		...

	@overload
	def y(self) -> NodeArray[ float ]:
		"""Returns a reference to the array storing y-coordinates of nodes."""
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

	@overload
	def bends(self, e : edge) -> DPolyline:
		"""Returns the bend point list of edgee."""
		...

	@overload
	def bends(self, e : edge) -> DPolyline:
		"""Returns the bend point list of edgee."""
		...

	def computePolyline(self, GC : GraphCopy, eOrig : edge, dpl : DPolyline) -> None:
		"""Returns the polyline of edgeeOrigindpl."""
		...

	def computePolylineClear(self, PG : PlanRep, eOrig : edge, dpl : DPolyline) -> None:
		"""Returns the polyline of edgeeOrigindpland clears the bend points of the copies."""
		...

	def computeBoundingBox(self, PG : PlanRep) -> DPoint:
		"""Computes the bounding box of the layout, which is a drawing ofPG."""
		...
