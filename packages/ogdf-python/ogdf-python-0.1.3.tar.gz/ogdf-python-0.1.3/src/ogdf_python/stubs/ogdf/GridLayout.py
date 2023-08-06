# file stubs/ogdf/GridLayout.py generated from classogdf_1_1_grid_layout
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
class GridLayout(object):

	"""Representation of a graph's grid layout."""

	#: The bend points of edges.
	m_bends : EdgeArray[IPolyline] = ...

	#: The x-coordinates of nodes.
	m_x : NodeArray[  int ] = ...

	#: The y-coordinates of nodes.
	m_y : NodeArray[  int ] = ...

	@overload
	def __init__(self) -> None:
		"""Creates an instance of a grid layout (associated with no graph)."""
		...

	@overload
	def __init__(self, G : Graph) -> None:
		"""Creates an instance of a grid layout associated withG."""
		...

	def __destruct__(self) -> None:
		"""Destruction."""
		...

	@overload
	def bends(self) -> EdgeArray[IPolyline]:
		"""Returns a reference to the array storing the bend points of edges."""
		...

	@overload
	def bends(self) -> EdgeArray[IPolyline]:
		"""Returns a reference to the array storing the bend points of edges."""
		...

	@overload
	def bends(self, e : edge) -> IPolyline:
		"""Returns a reference to the bend point list of edgee."""
		...

	@overload
	def bends(self, e : edge) -> IPolyline:
		"""Returns a reference to the bend point list of edgee."""
		...

	def checkLayout(self) -> bool:
		"""Checks if the grid layout is reasonable."""
		...

	def compactAllBends(self) -> None:
		"""Removes all unnecessary bends."""
		...

	def computeBoundingBox(self, xmin : int, xmax : int, ymin : int, ymax : int) -> None:
		"""Computes the bounding box of the grid layout."""
		...

	def getCompactBends(self, e : edge) -> IPolyline:
		"""Returns the bend point list of edgeewithout unnecessary bends."""
		...

	@overload
	def init(self) -> None:
		"""Initializes the grid layout for no graph (frees memory)."""
		...

	@overload
	def init(self, G : Graph) -> None:
		"""Initializes the grid layout for graphG."""
		...

	def manhattanEdgeLength(self, e : edge) -> int:
		...

	def maxManhattanEdgeLength(self) -> int:
		...

	def numberOfBends(self) -> int:
		"""Computes the total number of bends in the grid layout."""
		...

	def polyline(self, e : edge) -> IPolyline:
		"""Returns the polyline of edgee(including start and end point!)."""
		...

	def remap(self, drawing : Layout) -> None:
		"""Transforms the grid layout to a layout."""
		...

	def totalEdgeLength(self) -> float:
		"""Computes the total (euclidean) edge length of the grid layout."""
		...

	def totalManhattanEdgeLength(self) -> int:
		"""Computes the total manhattan edge length of the grid layout."""
		...

	@overload
	def x(self) -> NodeArray[  int ]:
		"""Returns a reference to the array storing the x-coordinates of nodes."""
		...

	@overload
	def x(self) -> NodeArray[  int ]:
		"""Returns a reference to the array storing the x-coordinates of nodes."""
		...

	@overload
	def x(self, v : node) -> int:
		"""Returns a reference to the x-coordinate of nodev."""
		...

	@overload
	def x(self, v : node) -> int:
		"""Returns a reference to the x-coordinate of nodev."""
		...

	@overload
	def y(self) -> NodeArray[  int ]:
		"""Returns a reference to the array storing the y-coordinates of nodes."""
		...

	@overload
	def y(self) -> NodeArray[  int ]:
		"""Returns a reference to the array storing the y-coordinates of nodes."""
		...

	@overload
	def y(self, v : node) -> int:
		"""Returns a reference to the y-coordinate of nodev."""
		...

	@overload
	def y(self, v : node) -> int:
		"""Returns a reference to the y-coordinate of nodev."""
		...

	def euclideanDistance(self, ip1 : IPoint, ip2 : IPoint) -> float:
		...

	def manhattanDistance(self, ip1 : IPoint, ip2 : IPoint) -> int:
		...
