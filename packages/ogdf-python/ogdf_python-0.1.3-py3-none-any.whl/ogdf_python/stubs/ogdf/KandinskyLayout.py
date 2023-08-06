# file stubs/ogdf/KandinskyLayout.py generated from classogdf_1_1_kandinsky_layout
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
class KandinskyLayout(ogdf.LayoutPlanRepUMLModule):

	"""Creates an orthogonal, planar drawing of an inputPlanRepUML. For nodes with a degree > 4, bends at the node are generated. The orthogonal representation is computed using an Integer Program. TheOrthoRepis compacted usingFlowCompaction."""

	def __init__(self) -> None:
		...

	def call(self, PG : PlanRepUML, adjExternal : adjEntry, drawing : Layout) -> None:
		"""Calls the layout algorithm. Input is a planarized representationPG, output is the layoutdrawing. Uses an IP to compute an orthogonal representation ofPG."""
		...

	@overload
	def separation(self) -> float:
		"""Returns the minimal allowed distance between edges and vertices."""
		...

	@overload
	def separation(self, sep : float) -> None:
		"""Sets the minimal allowed distance between edges and vertices tosep."""
		...

	def createExtension(self, emb : CombinatorialEmbedding, sol : float, ncols : int, H : Graph, embH : CombinatorialEmbedding, angles : AdjEntryArray[  int ], bends : AdjEntryArray[BendString], nodeRefs : NodeArray[node], nodeRefsBack : NodeArray[node], edgeRefs : EdgeArray[edge], edgeRefsBack : EdgeArray[edge], adjEntryOffsets : AdjEntryArray[ float ], adjEntryNumNeighbours : AdjEntryArray[  int ]) -> None:
		"""Creates the extension graphHfor the inputPlanRep, which has the property of having a degree4 required for the compaction step."""
		...

	def draw(self, PG : PlanRep, OR : OrthoRep, E : CombinatorialEmbedding, adjExternal : adjEntry, drawing : Layout) -> None:
		"""Assigns coordinates to the nodes and edges of the extension graph usingFlowCompaction. The resultingdrawingneeds to be adjusted to arrive at a drawing for the input graph of the main call."""
		...

	def getIP(self, emb : CombinatorialEmbedding) -> OsiSolverInterface:
		"""Generate an IP yielding the data for an orthogonal representation foremb."""
		...
