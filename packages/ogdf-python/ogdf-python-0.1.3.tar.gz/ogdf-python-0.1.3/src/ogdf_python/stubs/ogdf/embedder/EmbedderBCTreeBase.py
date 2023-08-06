# file stubs/ogdf/embedder/EmbedderBCTreeBase.py generated from classogdf_1_1embedder_1_1_embedder_b_c_tree_base
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
EnableLayers = TypeVar('EnableLayers')

class EmbedderBCTreeBase(ogdf.EmbedderModule, Generic[EnableLayers]):

	"""Common base for embedder algorithms based on BC trees."""

	#: an adjacency entry on the external face
	pAdjExternal : adjEntry = ...

	#: BC-tree of the original graph.
	pBCTree : BCTree = ...

	def initBCTree(self, G : Graph) -> node:
		"""InitializespBCTreeand returns the root node of this tree ornullptrifGis biconnected."""
		...

	def trivialInit(self, G : Graph) -> adjEntry:
		"""Initializationcode for biconnected input. Returns an adjacency entry that lies on the external face."""
		...
