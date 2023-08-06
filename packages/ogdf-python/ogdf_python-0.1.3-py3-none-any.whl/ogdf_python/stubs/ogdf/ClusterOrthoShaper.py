# file stubs/ogdf/ClusterOrthoShaper.py generated from classogdf_1_1_cluster_ortho_shaper
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
class ClusterOrthoShaper(object):

	"""Computes the orthogonal representation of a clustered graph."""

	class BendCost(enum.Enum):

		defaultCost = enum.auto()

		topDownCost = enum.auto()

		bottomUpCost = enum.auto()

	class n_type(enum.Enum):

		low = enum.auto()

		high = enum.auto()

		inner = enum.auto()

		outer = enum.auto()

	def __init__(self) -> None:
		...

	def __destruct__(self) -> None:
		...

	@overload
	def align(self) -> bool:
		...

	@overload
	def align(self, al : bool) -> None:
		...

	def bendCostTopDown(self, i : BendCost) -> None:
		...

	def call(self, PG : ClusterPlanRep, E : CombinatorialEmbedding, OR : OrthoRep, startBoundBendsPerEdge : int = 0, fourPlanar : bool = True) -> None:
		...

	def clusterProgBendCost(self, clDepth : int, treeDepth : int, pbc : int) -> int:
		...

	def clusterTradBendCost(self, clDepth : int, treeDepth : int, pbc : int) -> int:
		...

	@overload
	def distributeEdges(self) -> bool:
		"""returns option distributeEdges"""
		...

	@overload
	def distributeEdges(self, b : bool) -> None:
		"""sets option distributeEdges to b"""
		...

	@overload
	def fixDegreeFourAngles(self) -> bool:
		"""returns option for free angle assignment at degree four nodes"""
		...

	@overload
	def fixDegreeFourAngles(self, b : bool) -> None:
		"""sets option for free angle assignment at degree four nodes"""
		...

	@overload
	def multiAlign(self) -> bool:
		"""returns option multiAlign"""
		...

	@overload
	def multiAlign(self, b : bool) -> None:
		"""sets option multiAlign to b"""
		...

	@overload
	def traditional(self) -> bool:
		"""returns option for traditional angle distribution"""
		...

	@overload
	def traditional(self, b : bool) -> None:
		"""sets option traditional to b"""
		...
