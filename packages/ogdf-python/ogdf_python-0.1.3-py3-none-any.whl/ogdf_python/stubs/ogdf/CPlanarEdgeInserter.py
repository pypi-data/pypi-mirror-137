# file stubs/ogdf/CPlanarEdgeInserter.py generated from classogdf_1_1_c_planar_edge_inserter
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
class CPlanarEdgeInserter(object):

	"""Edge insertion algorithm for clustered graphs."""

	def __init__(self) -> None:
		...

	def __destruct__(self) -> None:
		...

	def call(self, CPR : ClusterPlanRep, E : CombinatorialEmbedding, G : Graph, origEdges : List[edge]) -> None:
		...

	def getPostProcessing(self) -> PostProcessType:
		...

	def setPostProcessing(self, p : PostProcessType) -> None:
		...

	def constructDualGraph(self, CPR : ClusterPlanRep, E : CombinatorialEmbedding, arcRightToLeft : EdgeArray[edge], arcLeftToRight : EdgeArray[edge], nodeOfFace : FaceArray[node], arcTwin : EdgeArray[edge]) -> None:
		...

	def findShortestPath(self, E : CombinatorialEmbedding, s : node, t : node, sDummy : node, tDummy : node, crossed : SList[adjEntry], nodeOfFace : FaceArray[node]) -> None:
		...

	def insertEdge(self, CPR : ClusterPlanRep, E : CombinatorialEmbedding, insertMe : edge, nodeOfFace : FaceArray[node], arcRightToLeft : EdgeArray[edge], arcLeftToRight : EdgeArray[edge], arcTwin : EdgeArray[edge], clusterOfFaceNode : NodeArray[cluster], crossed : SList[adjEntry]) -> None:
		...

	def postProcess(self) -> None:
		"""Use heuristics to improve the result if possible."""
		...

	def setArcStatus(self, eArc : edge, oSrc : node, oTgt : node, CG : ClusterGraph, clusterOfFaceNode : NodeArray[cluster], arcTwin : EdgeArray[edge]) -> None:
		...
