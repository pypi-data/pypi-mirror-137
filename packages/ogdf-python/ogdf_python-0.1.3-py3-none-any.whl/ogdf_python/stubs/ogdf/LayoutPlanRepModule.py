# file stubs/ogdf/LayoutPlanRepModule.py generated from classogdf_1_1_layout_plan_rep_module
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
class LayoutPlanRepModule(object):

	"""Interface for planar layout algorithms (used in the planarization approach)."""

	#: Stores the bounding box of the computed layout.
	m_boundingBox : DPoint = ...

	def __init__(self) -> None:
		"""Initializes a planar layout module."""
		...

	def __destruct__(self) -> None:
		"""Destructor."""
		...

	def call(self, PG : PlanRep, adjExternal : adjEntry, drawing : Layout) -> None:
		"""Computes a planar layout ofPGindrawing."""
		...

	def getBoundingBox(self) -> DPoint:
		"""Returns the bounding box of the computed layout."""
		...

	def __call__(self, PG : PlanRep, adjExternal : adjEntry, drawing : Layout) -> None:
		"""Computes a planar layout ofPGindrawing."""
		...

	@overload
	def separation(self) -> float:
		"""Returns the minimal allowed distance between edges and vertices."""
		...

	@overload
	def separation(self, sep : float) -> None:
		"""Sets the minimal allowed distance between edges and vertices tosep."""
		...

	def setBoundingBox(self, PG : PlanRep, drawing : Layout) -> None:
		"""Computes and sets the bounding box variablem_boundingBox."""
		...
