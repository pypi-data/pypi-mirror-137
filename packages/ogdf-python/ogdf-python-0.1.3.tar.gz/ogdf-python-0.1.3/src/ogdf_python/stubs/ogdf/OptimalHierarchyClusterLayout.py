# file stubs/ogdf/OptimalHierarchyClusterLayout.py generated from classogdf_1_1_optimal_hierarchy_cluster_layout
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
class OptimalHierarchyClusterLayout(ogdf.HierarchyClusterLayoutModule):

	"""The LP-based hierarchy cluster layout algorithm."""

	# Optional parameters

	@overload
	def nodeDistance(self) -> float:
		"""Returns the minimal allowed x-distance between nodes on a layer."""
		...

	@overload
	def nodeDistance(self, x : float) -> None:
		"""Sets the minimal allowed x-distance between nodes on a layer tox."""
		...

	@overload
	def layerDistance(self) -> float:
		"""Returns the minimal allowed y-distance between layers."""
		...

	@overload
	def layerDistance(self, x : float) -> None:
		"""Sets the minimal allowed y-distance between layers tox."""
		...

	@overload
	def fixedLayerDistance(self) -> bool:
		"""Returns the current setting of optionfixedLayerDistance."""
		...

	@overload
	def fixedLayerDistance(self, b : bool) -> None:
		"""Sets the optionfixedLayerDistancetob."""
		...

	@overload
	def weightSegments(self) -> float:
		"""Returns the weight of edge segments connecting to vertical segments."""
		...

	@overload
	def weightSegments(self, w : float) -> None:
		"""Sets the weight of edge segments connecting to vertical segments tow."""
		...

	@overload
	def weightBalancing(self) -> float:
		"""Returns the weight for balancing successors below a node; 0.0 means no balancing."""
		...

	@overload
	def weightBalancing(self, w : float) -> None:
		"""Sets the weight for balancing successors below a node tow; 0.0 means no balancing."""
		...

	@overload
	def weightClusters(self) -> float:
		"""Returns the weight for cluster boundary variables."""
		...

	@overload
	def weightClusters(self, w : float) -> None:
		"""Sets the weight for cluster boundary variables tow."""
		...

	@overload
	def __init__(self) -> None:
		"""Creates an instance of optimal hierarchy layout for clusters."""
		...

	@overload
	def __init__(self, _ : OptimalHierarchyClusterLayout) -> None:
		"""Copy constructor."""
		...

	def __destruct__(self) -> None:
		...

	def __assign__(self, _ : OptimalHierarchyClusterLayout) -> OptimalHierarchyClusterLayout:
		"""Assignment operator."""
		...

	def doCall(self, H : ExtendedNestingGraph, ACGC : ClusterGraphCopyAttributes) -> None:
		"""Implements the algorithm call."""
		...
