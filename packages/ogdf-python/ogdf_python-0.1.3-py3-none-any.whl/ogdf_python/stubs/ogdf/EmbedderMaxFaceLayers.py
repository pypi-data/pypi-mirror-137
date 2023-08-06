# file stubs/ogdf/EmbedderMaxFaceLayers.py generated from classogdf_1_1_embedder_max_face_layers
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
class EmbedderMaxFaceLayers(ogdf.embedder.LayersBlockEmbedder[ EmbedderMaxFace,  int ]):

	"""Embedder that maximizes the external face and optimizes the position of blocks afterwards."""

	def embedBlock(self, bT : node, cT : node, after : ListIterator[adjEntry]) -> None:
		"""Computes the adjacency list for all nodes in a block and calls recursively the function for all blocks incident to nodes in bT."""
		...

	def trivialInit(self, G : Graph) -> adjEntry:
		"""Initializationcode for biconnected input. Returns an adjacency entry that lies on the external face."""
		...
