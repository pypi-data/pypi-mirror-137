# file stubs/ogdf/NearestRectangleFinder/PairRectDist.py generated from structogdf_1_1_nearest_rectangle_finder_1_1_pair_rect_dist
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
class PairRectDist(object):

	"""Represents a rectangle (given by its index) and a distance value."""

	m_distance : float = ...

	m_index : int = ...

	@overload
	def __init__(self) -> None:
		...

	@overload
	def __init__(self, index : int, distance : float) -> None:
		...
