# file stubs/ogdf/EmbedderMinDepthMaxFace.py generated from classogdf_1_1_embedder_min_depth_max_face
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
class EmbedderMinDepthMaxFace(ogdf.EmbedderMaxFace):

	"""Embedding that minimizes block-nesting depth and maximizes the external face."""

	MDMFLengthAttribute : Type = embedder.MDMFLengthAttribute

	#: an array saving the length for each edge in the BC-tree
	cB : EdgeArray[  int ] = ...

	#: is saving for each edge of the block graph its length
	edgeLength : EdgeArray[MDMFLengthAttribute] = ...

	#: M2 is empty, if |M_B| != 1, otherwise M_B = {cH} M2 = {cH' in V_B \ {v} | m_B(cH') = m2} with m2 = max{m_B(vH) : vH in V_B, vH != cH}.
	M2 : NodeArray[List[node] ] = ...

	#: an array containing the maximum face size of each block
	maxFaceSize : NodeArray[  int ] = ...

	#: M_B = {cH in B | m_B(cH) = m_B} with m_B = max{m_B(c) : c in B} and m_B(c) = max( {0} cup {m_{c, B'} | c in B', B' != B} ).
	md_M_B : NodeArray[List[node] ] = ...

	#: saving for each node in the block graph its length
	md_nodeLength : NodeArray[  int ] = ...

	#: is saving for each node of the block graph its length
	mdmf_nodeLength : NodeArray[MDMFLengthAttribute] = ...

	#: is saving for each node of the block graph its cstrLength
	mf_cstrLength : NodeArray[  int ] = ...

	#: is saving for each node of the block graph its length
	mf_nodeLength : NodeArray[  int ] = ...

	#: an array containing the minimum depth of each block
	minDepth : NodeArray[  int ] = ...

	def doCall(self, G : Graph, adjExternal : adjEntry) -> None:
		"""Call embedder algorithm."""
		...

	def bottomUpTraversal(self, bT : node, cH : node) -> int:
		"""Bottom-up-traversal of bcTree computing the valuesm_{cT, bT} for all edges(cT, bT) in the BC-tree."""
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

	@overload
	def embedBlock(self, bT : node, cT : node, after : ListIterator[adjEntry]) -> None:
		"""Computes the adjacency list for all nodes in a block and calls recursively the function for all blocks incident to nodes in bT."""
		...

	def maximumFaceRec(self, bT : node, bT_opt : node, ell_opt : int) -> None:
		"""Top down traversal of BC-tree."""
		...

	def topDownTraversal(self, bT : node) -> None:
		"""Top-down-traversal of BC-tree."""
		...
