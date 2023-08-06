# file stubs/ogdf/TopologyModule.py generated from classogdf_1_1_topology_module
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
class TopologyModule(object):

	"""Constructs embeddings from given layout."""

	class Options(enum.Enum):

		"""The (pre/post)processing options."""

		#: should degree-one node's edge be crossed
		DegOneCrossings = enum.auto()

		#: should generalizations be turned into associations
		GenToAss = enum.auto()

		#: if there is a crossing between two edges with the same start or end point, should their position at the node be flipped and the crossing be skipped?
		CrossFlip = enum.auto()

		#: only flip if same edge type
		FlipUML = enum.auto()

		#: should loops between crossings (consecutive on both crossing edges) be deleted (we dont check for enclosed CC's; therefore it is safe to remove the crossing).
		Loop = enum.auto()

	def __init__(self) -> None:
		...

	def __destruct__(self) -> None:
		...

	def addOption(self, o : TopologyModule.Options) -> None:
		...

	def faceSum(self, PG : PlanRep, AG : GraphAttributes, f : face) -> float:
		...

	def getExternalFace(self, PG : PlanRep, AG : GraphAttributes) -> face:
		...

	def setEmbeddingFromGraph(self, PG : PlanRep, GA : GraphAttributes, adjExternal : adjEntry, setExternal : bool = True, reuseGAEmbedding : bool = False) -> bool:
		"""Uses the layoutGAto determine an embedding forPG."""
		...

	def setOptions(self, i : int) -> None:
		...

	def sortEdgesFromLayout(self, G : Graph, GA : GraphAttributes) -> None:
		"""Sorts the edges around all nodes ofGAcorresponding to the layout given inGA."""
		...

	def checkFlipCrossing(self, PG : PlanRep, v : node, flip : bool = True) -> bool:
		...

	def handleImprecision(self, PG : PlanRep) -> None:
		...

	def hasCrossing(self, legA : topology_module.EdgeLeg, legB : topology_module.EdgeLeg, xp : DPoint) -> bool:
		...

	def planarizeFromLayout(self, PG : PlanRep, AG : GraphAttributes) -> None:
		...

	def postProcess(self, PG : PlanRep) -> None:
		...

	def skipable(self, legA : topology_module.EdgeLeg, legB : topology_module.EdgeLeg) -> bool:
		...
