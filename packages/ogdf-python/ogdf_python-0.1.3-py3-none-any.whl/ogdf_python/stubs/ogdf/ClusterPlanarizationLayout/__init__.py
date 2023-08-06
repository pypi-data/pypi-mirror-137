# file stubs/ogdf/ClusterPlanarizationLayout/__init__.py generated from classogdf_1_1_cluster_planarization_layout
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
class ClusterPlanarizationLayout(object):

	"""The cluster planarization layout algorithm."""

	def __init__(self) -> None:
		"""Creates an instance of cluster planarization layout."""
		...

	def __destruct__(self) -> None:
		"""Destruction."""
		...

	@overload
	def call(self, G : Graph, acGraph : ClusterGraphAttributes, cGraph : ClusterGraph, simpleCConnect : bool = True) -> None:
		"""Calls cluster planarization layout with cluster-graph attributesacGraph."""
		...

	@overload
	def call(self, G : Graph, acGraph : ClusterGraphAttributes, cGraph : ClusterGraph, edgeWeight : EdgeArray[ float ], simpleCConnect : bool = True) -> None:
		"""Calls cluster planarization layout with cluster-graph attributesacGraph."""
		...

	@overload
	def pageRatio(self) -> float:
		"""Returns the current page ratio (= desired width / height of layout)."""
		...

	@overload
	def pageRatio(self, ratio : float) -> None:
		"""Sets the page ratio toratio."""
		...

	def setPacker(self, pPacker : CCLayoutPackModule) -> None:
		"""Sets the module option for the arrangement of connected components topPacker."""
		...

	def setPlanarLayouter(self, pPlanarLayouter : LayoutClusterPlanRepModule) -> None:
		"""Sets the module option for the planar layout algorithm topPlanarLayouter."""
		...

	def computeClusterPositions(self, CP : ClusterPlanRep, drawing : Layout, CA : HashArray[  int,ClusterPosition]) -> None:
		...
