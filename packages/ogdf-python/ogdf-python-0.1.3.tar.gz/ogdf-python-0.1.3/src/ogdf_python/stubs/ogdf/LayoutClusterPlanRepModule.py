# file stubs/ogdf/LayoutClusterPlanRepModule.py generated from classogdf_1_1_layout_cluster_plan_rep_module
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
class LayoutClusterPlanRepModule(object):

	"""Interface for planar cluster layout algorithms."""

	#: Stores the bounding box of the computed layout.
	m_boundingBox : DPoint = ...

	def __init__(self) -> None:
		"""Initializes a cluster planar layout module."""
		...

	def __destruct__(self) -> None:
		...

	def call(self, PG : ClusterPlanRep, adjExternal : adjEntry, drawing : Layout, origEdges : List[edge], originalGraph : Graph) -> None:
		"""Computes a layout ofPGindrawing."""
		...

	def getBoundingBox(self) -> DPoint:
		"""Returns the bounding box of the computed layout."""
		...

	def getOptions(self) -> int:
		"""Returns the (generic) options."""
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
