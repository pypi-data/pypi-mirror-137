# file stubs/ogdf/EdgeRouter.py generated from classogdf_1_1_edge_router
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
class EdgeRouter(object):

	"""Places node boxes in replacement areas of orthogonal drawing step and route edges to minimize bends."""

	@overload
	def __init__(self) -> None:
		...

	@overload
	def __init__(self, pru : PlanRep, H : OrthoRep, L : GridLayoutMapped, E : CombinatorialEmbedding, rou : RoutingChannel[  int ], med : MinimumEdgeDistances[  int ], nodewidth : NodeArray[  int ], nodeheight : NodeArray[  int ]) -> None:
		...

	def __destruct__(self) -> None:
		...

	def addbends(self, bs : BendString, s2 : str) -> None:
		...

	def addLeftBend(self, e : edge) -> edge:
		...

	def addRightBend(self, e : edge) -> edge:
		...

	def align(self, b : bool) -> None:
		"""set alignment option: place nodes in cage at outgoing generalization"""
		...

	@overload
	def call(self) -> None:
		"""places nodes in cages and routes incident edges"""
		...

	@overload
	def call(self, pru : PlanRep, H : OrthoRep, L : GridLayoutMapped, E : CombinatorialEmbedding, rou : RoutingChannel[  int ], med : MinimumEdgeDistances[  int ], nodewidth : NodeArray[  int ], nodeheight : NodeArray[  int ], align : bool = False) -> None:
		"""places nodes in cages and routes incident edges"""
		...

	def compute_gen_glue_points_x(self, v : node) -> None:
		"""compute glue points positions"""
		...

	def compute_gen_glue_points_y(self, v : node) -> None:
		"""compute glue points positions"""
		...

	def compute_glue_points_x(self, v : node) -> None:
		"""compute glue points positions"""
		...

	def compute_glue_points_y(self, v : node) -> None:
		"""compute glue points positions"""
		...

	def compute_place(self, v : node, inf : NodeInfo) -> None:
		"""computes placement"""
		...

	def compute_routing(self, v : node) -> None:
		"""computes routing after compute_place"""
		...

	def cp_x(self, ae : adjEntry) -> int:
		"""Returns assigned connection point (cage border) x-coordinate ofae's source."""
		...

	def cp_y(self, ae : adjEntry) -> int:
		"""Returns assigned connection point (cage border) y-coordinate ofae's source."""
		...

	def fix_position(self, v : node, x : int = 0, y : int = 0) -> None:
		"""same as set but updates m_fixed, coordinates cant be changed afterwards"""
		...

	def gp_x(self, ae : adjEntry) -> int:
		"""Returns assigned glue point (node border) x-coordinate."""
		...

	def gp_y(self, ae : adjEntry) -> int:
		"""Returns assigned glue point (node border) y-coordinate."""
		...

	def inEntry(self, inf : NodeInfo, d : OrthoDir, pos : int) -> adjEntry:
		"""adjEntries for edges in inLists"""
		...

	def init(self, pru : PlanRep, rou : RoutingChannel[  int ], align : bool = False) -> None:
		...

	def initialize_node_info(self, v : node, sep : int) -> None:
		"""sets values derivable from input"""
		...

	def multiDelta(self) -> None:
		"""for all multiple edges, set the delta value on both sides to minimum if not m_minDelta"""
		...

	def outEntry(self, inf : NodeInfo, d : OrthoDir, pos : int) -> adjEntry:
		"""adjEntries for edges in inLists"""
		...

	def place(self, v : node) -> None:
		"""applies precomputed placement"""
		...

	def set_position(self, v : node, x : int = 0, y : int = 0) -> None:
		"""sets position for node v in layout to value x,y, invoked to have central control over change"""
		...

	def setDistances(self) -> None:
		"""sets the computed distances in structure MinimumEdgeDistance m_med"""
		...
