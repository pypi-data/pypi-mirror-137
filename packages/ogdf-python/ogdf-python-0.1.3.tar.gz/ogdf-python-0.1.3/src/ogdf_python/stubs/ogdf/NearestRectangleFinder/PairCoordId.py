# file stubs/ogdf/NearestRectangleFinder/PairCoordId.py generated from structogdf_1_1_nearest_rectangle_finder_1_1_pair_coord_id
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
class PairCoordId(object):

	"""Represents a pair of a coordinate (x or y) and the index of a rectangle."""

	m_coord : float = ...

	m_index : int = ...

	@overload
	def __init__(self) -> None:
		...

	@overload
	def __init__(self, coord : float, index : int) -> None:
		...
