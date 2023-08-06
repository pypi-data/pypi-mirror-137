# file stubs/ogdf/FaceSinkGraph.py generated from classogdf_1_1_face_sink_graph
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
class FaceSinkGraph(ogdf.Graph):

	@overload
	def __init__(self) -> None:
		"""default constructor (dummy)"""
		...

	@overload
	def __init__(self, E : ConstCombinatorialEmbedding, s : node) -> None:
		"""constructor (we assume that the original graph is connected!)"""
		...

	def containsSource(self, v : node) -> bool:
		...

	@overload
	def faceNodeOf(self, e : edge) -> node:
		...

	@overload
	def faceNodeOf(self, f : face) -> node:
		...

	def init(self, E : ConstCombinatorialEmbedding, s : node) -> None:
		...

	def originalEmbedding(self) -> ConstCombinatorialEmbedding:
		"""returns a reference to the embedding E of the original graph G"""
		...

	def originalFace(self, v : node) -> face:
		"""returns the face in E corresponding to node v in the face-sink graph, 0 if v corresponds to a sink-switch"""
		...

	def originalGraph(self) -> Graph:
		"""return a reference to the original graph G"""
		...

	def originalNode(self, v : node) -> node:
		"""returns the sink-switch in G corresponding to node v in the face-sink graph, 0 if v corresponds to a face"""
		...

	def possibleExternalFaces(self, externalFaces : SList[face]) -> node:
		"""returns the list of faces f in E such that there exists an upward-planar drawing realizing E with f as external face a node v_T in tree T is returned as representative. v_T is 0 if no possible external face exists."""
		...

	def sinkSwitches(self, faceSwitches : FaceArray[List[adjEntry] ]) -> None:
		"""compute the sink switches of all faces."""
		...

	@overload
	def stAugmentation(self, h : node, G : Graph, superSink : node, augmentedEdges : SList[edge]) -> None:
		"""augments G to an st-planar graph"""
		...

	@overload
	def stAugmentation(self, h : node, G : Graph, augmentedNodes : SList[node], augmentedEdges : SList[edge]) -> None:
		"""augments G to an st-planar graph (original implementation)"""
		...
