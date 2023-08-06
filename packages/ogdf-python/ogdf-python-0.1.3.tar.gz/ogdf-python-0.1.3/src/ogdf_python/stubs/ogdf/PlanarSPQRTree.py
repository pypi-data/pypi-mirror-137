# file stubs/ogdf/PlanarSPQRTree.py generated from classogdf_1_1_planar_s_p_q_r_tree
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
class PlanarSPQRTree(ogdf.SPQRTree):

	"""SPQR-trees of planar graphs."""

	m_finished : bool = ...

	@overload
	def embed(self, G : Graph) -> None:
		"""EmbedsGaccording to the current embeddings of the skeletons ofT."""
		...

	@overload
	def embed(self, vT : node, x : int) -> None:
		"""Embeds the skeleton of the node vT with the specific embedding numbered by x."""
		...

	@overload
	def firstEmbedding(self, G : Graph) -> None:
		"""Embeds the original graphGcanonically by the indices of their adjEntries."""
		...

	@overload
	def nextEmbedding(self, G : Graph) -> bool:
		"""Embeds the original graphGwith the next embedding."""
		...

	@overload
	def numberOfEmbeddings(self) -> float:
		"""Returns the number of possible embeddings of G."""
		...

	@overload
	def numberOfEmbeddings(self, v : node) -> float:
		"""Returns the number of possible embeddings of the pertinent graph of nodev."""
		...

	def numberOfNodeEmbeddings(self, vT : node) -> int:
		"""Returns the number of possible embeddings of the skeleton of nodevT."""
		...

	@overload
	def randomEmbed(self) -> None:
		"""Embeds all skeleton graphs randomly."""
		...

	@overload
	def randomEmbed(self, G : Graph) -> None:
		"""Embeds all skeleton graphs randomly and embedsGaccording to the embeddings of the skeletons."""
		...

	@overload
	def reverse(self, vT : node) -> None:
		"""Flips the skeletonSofvTaround its poles."""
		...

	@overload
	def swap(self, vT : node, adj1 : adjEntry, adj2 : adjEntry) -> None:
		"""Exchanges the positions of the two edges corresponding toadj1andadj2in skeleton ofvT."""
		...

	@overload
	def swap(self, vT : node, e1 : edge, e2 : edge) -> None:
		"""Exchanges the positions of edgese1ande2in skeleton ofvT."""
		...

	def adoptEmbedding(self) -> None:
		...

	def createInnerVerticesEmbed(self, G : Graph, vT : node) -> None:
		...

	def expandVirtualEmbed(self, vT : node, adjVirt : adjEntry, adjEdges : SListPure[adjEntry]) -> None:
		...

	@overload
	def firstEmbedding(self, vT : node) -> None:
		...

	def init(self, isEmbedded : bool) -> None:
		"""Initialization(adaption of embeding)."""
		...

	@overload
	def nextEmbedding(self, it : ListIterator[node]) -> bool:
		...

	@overload
	def nextEmbedding(self, vT : node) -> bool:
		...

	@overload
	def reverse(self, nP : node, first : adjEntry, last : adjEntry) -> None:
		...

	def setPosInEmbedding(self, adjEdges : NodeArray[SListPure[adjEntry] ], currentCopy : NodeArray[node], lastAdj : NodeArray[adjEntry], current : SListPure[node], S : Skeleton, adj : adjEntry) -> None:
		...
