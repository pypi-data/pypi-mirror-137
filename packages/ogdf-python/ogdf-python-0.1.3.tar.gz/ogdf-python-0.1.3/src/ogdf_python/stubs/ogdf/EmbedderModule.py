# file stubs/ogdf/EmbedderModule.py generated from classogdf_1_1_embedder_module
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
class EmbedderModule(ogdf.Module, ogdf.Timeouter):

	"""Base class for embedder algorithms."""

	def __init__(self) -> None:
		"""Initializes an embedder module."""
		...

	def __destruct__(self) -> None:
		...

	def call(self, G : Graph, adjExternal : adjEntry) -> None:
		"""Calls the embedder algorithm for graphG."""
		...

	def __call__(self, G : Graph, adjExternal : adjEntry) -> None:
		"""Calls the embedder algorithm for graphG."""
		...

	def doCall(self, G : Graph, adjExternal : adjEntry) -> None:
		"""Calls the embedder algorithm for graphG."""
		...
