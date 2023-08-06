# file stubs/ogdf/ProcrustesPointSet.py generated from classogdf_1_1_procrustes_point_set
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
class ProcrustesPointSet(object):

	def __init__(self, numPoints : int) -> None:
		"""Constructor for allocating memory fornumPointspoints."""
		...

	def __destruct__(self) -> None:
		"""Destructor."""
		...

	def angle(self) -> float:
		"""Returns the rotation angle."""
		...

	def compare(self, other : ProcrustesPointSet) -> float:
		"""Calculates a value how good the two point sets match."""
		...

	def getX(self, i : int) -> float:
		"""Returnsi'thx-coordinate."""
		...

	def getY(self, i : int) -> float:
		"""Returnsi'thy-coordinate."""
		...

	def isFlipped(self) -> bool:
		"""Returns true if the point set is flipped by y coord."""
		...

	def normalize(self, flip : bool = False) -> None:
		"""Translates and scales the set such that the average center is 0, 0 and the average size is 1.0."""
		...

	def originX(self) -> float:
		"""Returns the origin's x."""
		...

	def originY(self) -> float:
		"""Returns the origin's y."""
		...

	def rotateTo(self, other : ProcrustesPointSet) -> None:
		"""Rotates the point set so it fits somehow onother."""
		...

	def scale(self) -> float:
		"""Returns the scale factor."""
		...

	def set(self, i : int, x : float, y : float) -> None:
		"""Setsi'thcoordinate."""
		...
