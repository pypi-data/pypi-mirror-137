# file stubs/ogdf/DominanceLayout.py generated from classogdf_1_1_dominance_layout
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
class DominanceLayout(ogdf.LayoutModule):

	def __init__(self) -> None:
		...

	def call(self, GA : GraphAttributes) -> None:
		"""Computes a layout of graphGA."""
		...

	def layout(self, GA : GraphAttributes, UPROrig : UpwardPlanRep) -> None:
		...

	def setMinGridDistance(self, dist : int) -> None:
		...

	def setUpwardPlanarizer(self, upPlanarizer : UpwardPlanarizerModule) -> None:
		...
