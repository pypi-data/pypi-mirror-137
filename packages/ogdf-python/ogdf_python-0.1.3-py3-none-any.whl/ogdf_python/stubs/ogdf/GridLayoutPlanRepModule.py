# file stubs/ogdf/GridLayoutPlanRepModule.py generated from classogdf_1_1_grid_layout_plan_rep_module
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
class GridLayoutPlanRepModule(ogdf.PlanarGridLayoutModule):

	"""Base class for grid layout algorithms operating on aPlanRep."""

	def __init__(self) -> None:
		"""Initializes a plan-rep grid layout module."""
		...

	def __destruct__(self) -> None:
		...

	@overload
	def callGrid(self, G : Graph, gridLayout : GridLayout) -> None:
		"""Calls the grid layout algorithm (call forGridLayout)."""
		...

	@overload
	def callGrid(self, PG : PlanRep, gridLayout : GridLayout) -> None:
		"""Calls the grid layout algorithm (call forGridLayoutof aPlanRep)."""
		...

	@overload
	def callGridFixEmbed(self, G : Graph, gridLayout : GridLayout, adjExternal : adjEntry = None) -> None:
		"""Calls the grid layout algorithm with a fixed planar embedding (call forGridLayout)."""
		...

	@overload
	def callGridFixEmbed(self, PG : PlanRep, gridLayout : GridLayout, adjExternal : adjEntry = None) -> None:
		"""Calls the grid layout algorithm with a fixed planar embedding (call forGridLayoutof aPlanRep)."""
		...

	@overload
	def doCall(self, G : Graph, adjExternal : adjEntry, gridLayout : GridLayout, boundingBox : IPoint, fixEmbedding : bool) -> None:
		"""ImplementsPlanarGridLayoutModule::doCall()."""
		...

	@overload
	def doCall(self, G : Graph, adjExternal : adjEntry, gridLayout : GridLayout, boundingBox : IPoint, fixEmbedding : bool) -> None:
		"""Implements the algorithm call."""
		...

	@overload
	def doCall(self, G : Graph, gridLayout : GridLayout, boundingBox : IPoint) -> None:
		"""Implements theGridLayoutModule::doCall()."""
		...

	@overload
	def doCall(self, PG : PlanRep, adjExternal : adjEntry, gridLayout : GridLayout, boundingBox : IPoint, fixEmbedding : bool) -> None:
		"""Implements the algorithm call."""
		...
