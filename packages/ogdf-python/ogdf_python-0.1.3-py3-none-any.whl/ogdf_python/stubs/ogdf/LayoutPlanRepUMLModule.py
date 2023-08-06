# file stubs/ogdf/LayoutPlanRepUMLModule.py generated from classogdf_1_1_layout_plan_rep_u_m_l_module
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
class LayoutPlanRepUMLModule(object):

	"""Interface for planar UML layout algorithms."""

	#: Stores the bounding box of the computed layout.
	m_boundingBox : DPoint = ...

	def __init__(self) -> None:
		"""Initializes a UML planar layout module."""
		...

	def __destruct__(self) -> None:
		...

	def call(self, PG : PlanRepUML, adjExternal : adjEntry, drawing : Layout) -> None:
		"""Computes a planar layout ofPGindrawing."""
		...

	def getBoundingBox(self) -> DPoint:
		"""Returns the bounding box of the computed layout."""
		...

	def getOptions(self) -> int:
		"""Returns the (generic) options."""
		...

	def __call__(self, PG : PlanRepUML, adjExternal : adjEntry, drawing : Layout) -> None:
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

	def setOptions(self, _ : int) -> None:
		"""Sets the (generic) options; derived classes have to cope with the interpretation)"""
		...

	def setBoundingBox(self, PG : PlanRep, drawing : Layout) -> None:
		"""Computes and sets the bounding box variablem_boundingBox."""
		...
