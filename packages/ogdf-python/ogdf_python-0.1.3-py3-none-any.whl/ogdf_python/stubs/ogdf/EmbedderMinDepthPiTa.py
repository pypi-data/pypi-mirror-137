# file stubs/ogdf/EmbedderMinDepthPiTa.py generated from classogdf_1_1_embedder_min_depth_pi_ta
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
class EmbedderMinDepthPiTa(ogdf.embedder.EmbedderBCTreeBase[ False ]):

	"""Embedder that minimizes block-nesting depth for given embedded blocks."""

	def __init__(self) -> None:
		...

	def doCall(self, G : Graph, adjExternal : adjEntry) -> None:
		"""Computes an embedding ofG."""
		...

	@overload
	def useExtendedDepthDefinition(self) -> bool:
		...

	@overload
	def useExtendedDepthDefinition(self, b : bool) -> None:
		...

	def trivialInit(self, G : Graph) -> adjEntry:
		"""Initializationcode for biconnected input. Returns an adjacency entry that lies on the external face."""
		...
