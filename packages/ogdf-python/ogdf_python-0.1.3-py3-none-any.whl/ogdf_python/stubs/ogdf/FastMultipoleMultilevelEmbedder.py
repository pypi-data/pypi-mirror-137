# file stubs/ogdf/FastMultipoleMultilevelEmbedder.py generated from classogdf_1_1_fast_multipole_multilevel_embedder
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
class FastMultipoleMultilevelEmbedder(ogdf.LayoutModule):

	"""The fast multipole multilevel embedder approach for force-directed multilevel layout."""

	def __init__(self) -> None:
		"""Constructor, just sets number of maximum threads."""
		...

	def call(self, GA : GraphAttributes) -> None:
		"""Calls the algorithm for graphGAand returns the layout information inGA."""
		...

	def maxNumThreads(self, numThreads : int) -> None:
		...

	def multilevelUntilNumNodesAreLess(self, nodesBound : int) -> None:
		"""sets the bound for the number of nodes for multilevel step"""
		...
