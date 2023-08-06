# file stubs/ogdf/PlanarizationLayoutUML.py generated from classogdf_1_1_planarization_layout_u_m_l
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
class PlanarizationLayoutUML(ogdf.UMLLayoutModule):

	"""The planarization layout algorithm."""

	# Algorithm call

	@overload
	def call(self, GA : GraphAttributes) -> None:
		"""Calls planarization layout forGraphAttributesGAand computes a layout."""
		...

	@overload
	def call(self, umlGraph : UMLGraph) -> None:
		"""Calls planarization layout for UML-graphumlGraphand computes a mixed-upward layout."""
		...

	@overload
	def simpleCall(self, umlGraph : UMLGraph) -> None:
		"""Simple call function that does not care about cliques etc."""
		...

	@overload
	def simpleCall(self, GA : GraphAttributes) -> None:
		"""Simple call function."""
		...

	def callIncremental(self, umlgraph : UMLGraph, fixedNodes : NodeArray[ bool ], fixedEdges : EdgeArray[ bool ]) -> None:
		"""Incremental call function."""
		...

	# Optional parameters

	@overload
	def pageRatio(self) -> float:
		"""Returns the current setting of option pageRatio."""
		...

	@overload
	def pageRatio(self, ratio : float) -> None:
		"""Sets the option pageRatio toratio."""
		...

	def setLayouterOptions(self, ops : int) -> None:
		...

	def alignSons(self, b : bool) -> None:
		...

	# Module options

	def setCrossMin(self, pCrossMin : UMLCrossingMinimizationModule) -> None:
		"""Sets the module option for UML crossing minimization."""
		...

	def setEmbedder(self, pEmbedder : EmbedderModule) -> None:
		"""Sets the module option for the graph embedding algorithm."""
		...

	def setPlanarLayouter(self, pPlanarLayouter : LayoutPlanRepUMLModule) -> None:
		"""Sets the module option for the planar layout algorithm."""
		...

	def setPacker(self, pPacker : CCLayoutPackModule) -> None:
		"""Sets the module option for the arrangement of connected components."""
		...

	# Further information

	def numberOfCrossings(self) -> int:
		"""Returns the number of crossings in computed layout."""
		...

	def assureDrawability(self, umlGraph : UMLGraph) -> None:
		...

	def __init__(self) -> None:
		"""Creates an instance of planarization layout and sets options to default values."""
		...

	def __destruct__(self) -> None:
		...

	def arrangeCCs(self, PG : PlanRep, GA : GraphAttributes, boundingBox : Array[DPoint]) -> None:
		...

	def doSimpleCall(self, GA : GraphAttributes) -> None:
		...

	def getFixationDistance(self, startNode : node, distance : HashArray[  int,  int ], fixedNodes : NodeArray[ bool ]) -> None:
		...

	def postProcess(self, UG : UMLGraph) -> None:
		...

	def preProcess(self, UG : UMLGraph) -> None:
		...

	def reembed(self, PG : PlanRepUML, ccNumber : int, l_align : bool = False, l_gensExist : bool = False) -> None:
		...

	def sortIncrementalNodes(self, addNodes : List[node], fixedNodes : NodeArray[ bool ]) -> None:
		...
