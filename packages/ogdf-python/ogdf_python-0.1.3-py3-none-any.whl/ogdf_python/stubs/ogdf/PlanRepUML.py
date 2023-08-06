# file stubs/ogdf/PlanRepUML.py generated from classogdf_1_1_plan_rep_u_m_l
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
class PlanRepUML(ogdf.PlanRep):

	"""Planarized representation (of a connected component) of aUMLGraph; allows special handling of hierarchies in the graph."""

	@overload
	def __init__(self, umlGraph : UMLGraph) -> None:
		"""Construction."""
		...

	@overload
	def __init__(self, GA : GraphAttributes) -> None:
		...

	# Incremental drawing

	def setupIncremental(self, indexCC : int, E : CombinatorialEmbedding) -> None:
		"""Initializes incremental stuff, e.g. insert incremental mergers."""
		...

	def incrementalMergers(self, indexCC : int) -> SList[node]:
		"""Returns the list of inserted incremental mergers."""
		...

	# Set generic types

	@overload
	def alignUpward(self, ae : adjEntry) -> bool:
		...

	@overload
	def alignUpward(self, ae : adjEntry, b : bool) -> None:
		...

	# Structural alterations

	def insertGenMerger(self, v : node, inGens : SList[edge], E : CombinatorialEmbedding) -> node:
		"""Inserts a generalization merge node for all incoming generalizations ofvand returns its conserving embedding."""
		...

	def expand(self, lowDegreeExpand : bool = False) -> None:
		"""Expands nodes with degree > 4 and merge nodes for generalizations."""
		...

	def expandLowDegreeVertices(self, OR : OrthoRep, alignSmallDegree : bool = False) -> None:
		"""Expands nodes with degree <= 4 and aligns opposite edges at degree 2 nodes."""
		...

	def collapseVertices(self, OR : OrthoRep, drawing : Layout) -> None:
		...

	# Extension of methods defined by GraphCopy/PlanRep

	def split(self, e : edge) -> edge:
		"""Splits edge e."""
		...

	@overload
	def writeGML(self, fileName : str, drawing : Layout) -> None:
		"""Writes attributed graph in GML format to filefileName(for debugging only)"""
		...

	@overload
	def writeGML(self, fileName : str) -> None:
		...

	@overload
	def writeGML(self, fileName : str, AG : GraphAttributes) -> None:
		...

	@overload
	def writeGML(self, os : std.ostream, drawing : Layout) -> None:
		"""Writes attributed graph in GML format to output streamos(for debugging only)"""
		...

	@overload
	def writeGML(self, fileName : str, OR : OrthoRep, drawing : Layout) -> None:
		...

	@overload
	def writeGML(self, os : std.ostream, OR : OrthoRep, drawing : Layout) -> None:
		...

	@overload
	def writeGML(self, fileName : str, OR : OrthoRep, drawing : GridLayoutMapped) -> None:
		...

	@overload
	def writeGML(self, os : std.ostream, OR : OrthoRep, drawing : GridLayoutMapped) -> None:
		...

	m_alignUpward : AdjEntryArray[ bool ] = ...

	def __destruct__(self) -> None:
		"""Deconstruction."""
		...

	def faceSplitter(self, e : edge) -> bool:
		"""Returns true if an edge splits a face into two subfaces to guarantee generalizations to be on opposite sides of a node."""
		...

	def getUMLGraph(self) -> UMLGraph:
		...

	def initCC(self, i : int) -> None:
		...

	def removeFaceSplitter(self) -> None:
		"""Removes all face splitting edges."""
		...

	def prepareIncrementalMergers(self, indexCC : int, E : CombinatorialEmbedding) -> None:
		...
