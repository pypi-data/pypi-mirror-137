# file stubs/ogdf/EmbedderMaxFace.py generated from classogdf_1_1_embedder_max_face
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
T = TypeVar('T')

class EmbedderMaxFace(ogdf.embedder.EmbedderBCTreeBase[ False ]):

	"""Embedder that maximizes the external face."""

	#: all blocks
	blockG : NodeArray[Graph] = ...

	#: is saving for each node in the block graphs its cstrLength
	cstrLength : NodeArray[NodeArray[  int ] ] = ...

	#: a mapping of edges in blockG to the auxiliaryGraph of the BC-tree
	eBlockEmbedding_to_eH : NodeArray[EdgeArray[edge] ] = ...

	#: a mapping of edges in the auxiliaryGraph of the BC-tree to blockG
	eH_to_eBlockEmbedding : NodeArray[EdgeArray[edge] ] = ...

	#: a mapping of nodes in blockG to the auxiliaryGraph of the BC-tree
	nBlockEmbedding_to_nH : NodeArray[NodeArray[node] ] = ...

	#: saves for every node of PG the new adjacency list
	newOrder : NodeArray[List[adjEntry] ] = ...

	#: a mapping of nodes in the auxiliaryGraph of the BC-tree to blockG
	nH_to_nBlockEmbedding : NodeArray[NodeArray[node] ] = ...

	#: saving for each node in the block graphs its length
	nodeLength : NodeArray[NodeArray[  int ] ] = ...

	#: The SPQR-trees of the blocks.
	spqrTrees : NodeArray[StaticSPQRTree] = ...

	#: treeNodeTreated saves for all block nodes in the BC-tree if it has already been treated or not.
	treeNodeTreated : NodeArray[ bool ] = ...

	def doCall(self, G : Graph, adjExternal : adjEntry) -> None:
		"""Computes an embedding ofGwith maximum external face."""
		...

	def computeBlockGraphs(self, bT : node, cH : node) -> None:
		"""Computes recursively the block graph for every block."""
		...

	def computeNodeLength(self, bT : node, setter : Callable) -> None:
		...

	def constraintMaxFace(self, bT : node, cH : node) -> int:
		"""Bottom up traversal of BC-tree."""
		...

	@overload
	def embedBlock(self, bT : node) -> None:
		"""Computes the adjacency list for all nodes in a block and calls recursively the function for all blocks incident to nodes in bT."""
		...

	@overload
	def embedBlock(self, bT : node, cT : node, after : ListIterator[adjEntry]) -> None:
		"""Computes the adjacency list for all nodes in a block and calls recursively the function for all blocks incident to nodes in bT."""
		...

	def forEachIngoingNeighbor(self, v : node, fun : Callable) -> None:
		"""Callsfunfor every ingoing edge (w,v)."""
		...

	def internalEmbedBlock(self, bT : node, cT : node, after : ListIterator[adjEntry], blockGraph : Graph, paramNodeLength : NodeArray[ T ], paramEdgeLength : EdgeArray[ T ], mapNodeToH : NodeArray[node], mapEdgeToH : EdgeArray[edge], nodeInBlock : node) -> None:
		...

	def internalMaximumFaceRec(self, bT : node, bT_opt : node, ell_opt : int, blockGraph : Graph, paramNodeLength : NodeArray[  int ], spqrTree : StaticSPQRTree, getBENode : Callable, getCstrLength : Callable, getNodeLength : Callable, maxFaceSizeToUpdate : int = None) -> None:
		...

	def maximumFaceRec(self, bT : node, bT_opt : node, ell_opt : int) -> None:
		"""Top down traversal of BC-tree."""
		...
