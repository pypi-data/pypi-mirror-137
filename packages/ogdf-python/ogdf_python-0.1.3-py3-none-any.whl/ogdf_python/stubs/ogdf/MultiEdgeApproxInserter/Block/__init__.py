# file stubs/ogdf/MultiEdgeApproxInserter/Block/__init__.py generated from classogdf_1_1_multi_edge_approx_inserter_1_1_block
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
class Block(ogdf.Graph):

	#: allocation nodes
	m_allocNodes : NodeArray[ArrayBuffer[node] ] = ...

	#: maps adjacency entries in block to original graph
	m_BCtoG : AdjEntryArray[adjEntry] = ...

	#: costs of an edge (as given for edges in original graph)
	m_cost : EdgeArray[  int ] = ...

	#: insertion path in SPQR-tree
	m_pathSPQR : Array[SPQRPath] = ...

	def __init__(self) -> None:
		...

	def __destruct__(self) -> None:
		...

	def computeTraversingCosts(self, n : node, e1 : edge, e2 : edge) -> None:
		...

	def constructDualBlock(self) -> None:
		...

	def cost(self, e : edge) -> int:
		...

	def costsSubpath(self, n : node, eIn : edge, eOut : edge, s : node, t : node, dirFrom : PathDir, dirTo : PathDir) -> int:
		...

	def embPrefAgree(self, n : node, p_pick : EmbeddingPreference, p_e : EmbeddingPreference) -> bool:
		...

	def findBestFace(self, s : node, t : node, len : int) -> adjEntry:
		...

	def findBestFaces(self, s : node, t : node, adj_s : adjEntry, adj_t : adjEntry) -> int:
		...

	def findShortestPath(self, n : node, eRef : edge) -> int:
		...

	def initSPQR(self, m : int) -> None:
		...

	def isBridge(self) -> bool:
		...

	def pathToArray(self, i : int, path : Array[PathElement]) -> None:
		...

	@overload
	def spqr(self) -> StaticPlanarSPQRTree:
		...

	@overload
	def spqr(self) -> StaticPlanarSPQRTree:
		...

	def switchingPair(self, n : node, m : node, p_pick_n : EmbeddingPreference, p_n : EmbeddingPreference, p_pick_m : EmbeddingPreference, p_m : EmbeddingPreference) -> bool:
		...
