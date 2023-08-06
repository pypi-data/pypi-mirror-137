# file stubs/ogdf/UMLGraph/__init__.py generated from classogdf_1_1_u_m_l_graph
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
class UMLGraph(ogdf.GraphAttributes):

	# Structural changes

	def insertGenMergers(self) -> None:
		"""Merges generalizations at a common superclass."""
		...

	def doInsertMergers(self, v : node, inGens : SList[edge]) -> node:
		"""Inserts mergers per node with given edges."""
		...

	def undoGenMergers(self) -> None:
		...

	# Cliques

	@overload
	def replaceByStar(self, cliques : List[List[node] ]) -> None:
		"""Replaces (dense) subgraphs given in list clique by inserting a center node connected to each node (=>star) and deleting all edges between nodes in clique returns center node."""
		...

	def undoStars(self) -> None:
		"""Undo clique replacements."""
		...

	def undoStar(self, center : node, restoreAllEdges : bool) -> None:
		"""Boolean switches restore of all hidden edges in single clique call."""
		...

	def cliqueRect(self, v : node) -> DRect:
		"""Returns the size of a circular drawing for a clique around center v."""
		...

	def cliquePos(self, v : node) -> DPoint:
		...

	def computeCliquePosition(self, adjNodes : List[node], center : node, rectMin : float = -1.0) -> None:
		"""Compute positions for the nodes in adjNodes on a circle."""
		...

	def centerNodes(self) -> SListPure[node]:
		...

	def setDefaultCliqueCenterSize(self, i : float) -> None:
		"""Default size of inserted clique replacement center nodes."""
		...

	def getDefaultCliqueCenterSize(self) -> float:
		...

	def isReplacement(self, e : edge) -> bool:
		"""Returns true if edge was inserted during clique replacement."""
		...

	@overload
	def replaceByStar(self, clique : List[node], cliqueNum : NodeArray[  int ]) -> node:
		...

	def circularBound(self, center : node) -> DRect:
		...

	# Only set and updated in insertgenmergers

	@overload
	def __init__(self) -> None:
		...

	@overload
	def __init__(self, G : Graph, initAttributes : int = 0) -> None:
		"""By default, all edges are associations."""
		...

	def __destruct__(self) -> None:
		"""Destructor."""
		...

	def adjustHierarchyParents(self) -> None:
		"""Adjusts the parent field for all nodes after insertion of mergers. If insertion is done per node via doinsert, adjust has to be called afterwards. Otherwise, insertgenmergers calls it."""
		...

	def assClass(self, e : edge) -> AssociationClass:
		...

	def assClassList(self) -> SListPure[AssociationClass]:
		...

	def createAssociationClass(self, e : edge, width : float = 1.0, height : float = 1.0) -> node:
		"""Adds association class to edge e."""
		...

	@overload
	def init(self, G : Graph, attr : int) -> None:
		"""Initializes the graph attributes for graphG."""
		...

	@overload
	def init(self, G : Graph, initAttr : int) -> None:
		...

	def modelAssociationClass(self, ac : AssociationClass) -> node:
		...

	def modelAssociationClasses(self) -> None:
		"""Inserts representation for association class in underlying graph."""
		...

	def setUpwards(self, a : adjEntry, b : bool) -> None:
		"""Sets status of edges to be specially embedded (if alignment)"""
		...

	def undoAssociationClass(self, ac : AssociationClass) -> None:
		"""Removes the modeling of the association class without removing the information."""
		...

	def undoAssociationClasses(self) -> None:
		...

	def upwards(self, a : adjEntry) -> bool:
		...

	@overload
	def writeGML(self, fileName : str) -> None:
		"""Writes attributed graph in GML format to file fileName."""
		...

	@overload
	def writeGML(self, os : std.ostream) -> None:
		"""Writes attributed graph in GML format to output stream os."""
		...
