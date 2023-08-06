# file stubs/ogdf/EmbedderMaxFaceBiconnectedGraphsLayers.py generated from classogdf_1_1_embedder_max_face_biconnected_graphs_layers
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
T = TypeVar('T')

class EmbedderMaxFaceBiconnectedGraphsLayers(ogdf.EmbedderMaxFaceBiconnectedGraphs[ T ], Generic[T]):

	"""Embedder that maximizes the external face (plus layers approach)."""

	def embed(self, G : Graph, adjExternal : adjEntry, nodeLength : NodeArray[ T ], edgeLength : EdgeArray[ T ], n : node = None) -> None:
		"""EmbedsGby computing and extending a maximum face inGcontainingn."""
		...
