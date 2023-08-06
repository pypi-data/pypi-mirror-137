# file stubs/ogdf/NonPlanarCore/CutEdge.py generated from structogdf_1_1_non_planar_core_1_1_cut_edge
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
class CutEdge(object):

	"""Struct to represent an edge that needs to be crossed in order to cross an st-component."""

	#: true, iff the edge is directed from thespartition to thetpartion
	dir : bool = ...

	#: the edge
	e : edge = ...

	def __init__(self, paramEdge : edge, directed : bool) -> None:
		...
