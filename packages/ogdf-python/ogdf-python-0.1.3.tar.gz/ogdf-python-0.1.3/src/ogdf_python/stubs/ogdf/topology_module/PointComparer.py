# file stubs/ogdf/topology_module/PointComparer.py generated from classogdf_1_1topology__module_1_1_point_comparer
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
class PointComparer(ogdf.GenericComparer[ ListIterator[ EdgeLeg  ], float ]):

	"""Sorts EdgeLegs according to their xp distance to a reference point."""

	def __init__(self, refPoint : DPoint) -> None:
		...
