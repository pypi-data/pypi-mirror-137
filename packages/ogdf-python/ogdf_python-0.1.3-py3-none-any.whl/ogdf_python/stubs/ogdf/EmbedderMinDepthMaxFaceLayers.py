# file stubs/ogdf/EmbedderMinDepthMaxFaceLayers.py generated from classogdf_1_1_embedder_min_depth_max_face_layers
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
class EmbedderMinDepthMaxFaceLayers(ogdf.embedder.LayersBlockEmbedder[ EmbedderMinDepthMaxFace, embedder.MDMFLengthAttribute ]):

	"""Planar graph embedding that minimizes block-nesting depth and maximizes the external face and optimizes the position of blocks afterwards."""

	def embedBlock(self, bT : node, cT : node, after : ListIterator[adjEntry]) -> None:
		"""Computes the adjacency list for all nodes in a block and calls recursively the function for all blocks incident to nodes in bT."""
		...
