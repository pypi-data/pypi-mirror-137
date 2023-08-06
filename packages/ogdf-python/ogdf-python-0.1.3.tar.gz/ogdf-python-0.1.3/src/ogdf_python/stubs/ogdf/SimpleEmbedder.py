# file stubs/ogdf/SimpleEmbedder.py generated from classogdf_1_1_simple_embedder
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
class SimpleEmbedder(ogdf.EmbedderModule):

	"""Embedder that chooses a largest face as the external one."""

	def __init__(self) -> None:
		...

	def __destruct__(self) -> None:
		...

	def doCall(self, G : Graph, adjExternal : adjEntry) -> None:
		"""Call embedder algorithm."""
		...
