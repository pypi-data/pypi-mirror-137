# file stubs/ogdf/EmbedderMinDepth.py generated from classogdf_1_1_embedder_min_depth
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
class EmbedderMinDepth(ogdf.embedder.EmbedderBCTreeBase[ False ]):

	"""Embedder that minimizes block-nesting depth."""

	def doCall(self, G : Graph, adjExternal : adjEntry) -> None:
		"""Computes an embedding ofGwith minimum depth."""
		...
