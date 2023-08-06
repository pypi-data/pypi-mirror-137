# file stubs/ogdf/energybased/fmmm/MAARPacking.py generated from classogdf_1_1energybased_1_1fmmm_1_1_m_a_a_r_packing
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
class MAARPacking(object):

	"""data structure for packing rectangles within an area of a desired aspect ratio without overlappings; optimization goal: to minimize the used aspect ratio area"""

	def __init__(self) -> None:
		"""constructor"""
		...

	def __destruct__(self) -> None:
		"""destructor"""
		...

	def pack_rectangles_using_Best_Fit_strategy(self, R : List[Rectangle], aspect_ratio : float, presort : FMMMOptions.PreSort, allow_tipping_over : FMMMOptions.TipOver, aspect_ratio_area : float, bounding_rectangles_area : float) -> None:
		"""The rectangles in R are packed using the First Fit tiling stratey (precisely the new down left corner coordinate of each rectangle is calculated and stored in R). The aspect ratio area and the area of the bounding rectangles are calculated, too."""
		...
