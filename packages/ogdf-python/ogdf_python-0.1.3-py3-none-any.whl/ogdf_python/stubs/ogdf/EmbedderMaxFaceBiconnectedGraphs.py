# file stubs/ogdf/EmbedderMaxFaceBiconnectedGraphs.py generated from classogdf_1_1_embedder_max_face_biconnected_graphs
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
T = TypeVar('T')

class EmbedderMaxFaceBiconnectedGraphs(Generic[T]):

	"""Embedder that maximizing the external face."""

	def compute(self, G : Graph, nodeLength : NodeArray[ T ], edgeLength : EdgeArray[ T ], spqrTree : StaticSPQRTree, edgeLengthSkel : NodeArray[EdgeArray[ T ] ]) -> None:
		"""Computes the component lengths of all virtual edges in spqrTree."""
		...

	@overload
	def computeSize(self, G : Graph, n : node, nodeLength : NodeArray[ T ], edgeLength : EdgeArray[ T ]) -> T:
		"""Returns the size of a maximum external face inGcontaining the noden."""
		...

	@overload
	def computeSize(self, G : Graph, n : node, nodeLength : NodeArray[ T ], edgeLength : EdgeArray[ T ], spqrTree : StaticSPQRTree) -> T:
		"""Returns the size of a maximum external face inGcontaining the noden."""
		...

	@overload
	def computeSize(self, G : Graph, n : node, nodeLength : NodeArray[ T ], edgeLength : EdgeArray[ T ], spqrTree : StaticSPQRTree, edgeLengthSkel : NodeArray[EdgeArray[ T ] ]) -> T:
		"""Returns the size of a maximum external face inGcontaining the noden."""
		...

	@overload
	def computeSize(self, G : Graph, nodeLength : NodeArray[ T ], edgeLength : EdgeArray[ T ]) -> T:
		"""Returns the size of a maximum external face inG."""
		...

	@overload
	def computeSize(self, G : Graph, nodeLength : NodeArray[ T ], edgeLength : EdgeArray[ T ], spqrTree : StaticSPQRTree, edgeLengthSkel : NodeArray[EdgeArray[ T ] ]) -> T:
		"""Returns the size of a maximum external face inG."""
		...

	def embed(self, G : Graph, adjExternal : adjEntry, nodeLength : NodeArray[ T ], edgeLength : EdgeArray[ T ], n : node = None) -> None:
		"""EmbedsGby computing and extending a maximum face inGcontainingn."""
		...

	def adjEntryForNode(self, ae : adjEntry, before : ListIterator[adjEntry], spqrTree : StaticSPQRTree, treeNodeTreated : NodeArray[ bool ], mu : node, leftNode : node, nodeLength : NodeArray[ T ], edgeLength : NodeArray[EdgeArray[ T ] ], newOrder : NodeArray[List[adjEntry] ], adjBeforeNodeArraySource : NodeArray[ListIterator[adjEntry] ], adjBeforeNodeArrayTarget : NodeArray[ListIterator[adjEntry] ], adjExternal : adjEntry) -> None:
		...

	def bottomUpTraversal(self, spqrTree : StaticSPQRTree, mu : node, nodeLength : NodeArray[ T ], edgeLength : NodeArray[EdgeArray[ T ] ]) -> None:
		"""Bottom up traversal of SPQR-tree computing the component length of all non-reference edges."""
		...

	def expandEdge(self, spqrTree : StaticSPQRTree, treeNodeTreated : NodeArray[ bool ], mu : node, leftNode : node, nodeLength : NodeArray[ T ], edgeLength : NodeArray[EdgeArray[ T ] ], newOrder : NodeArray[List[adjEntry] ], adjBeforeNodeArraySource : NodeArray[ListIterator[adjEntry] ], adjBeforeNodeArrayTarget : NodeArray[ListIterator[adjEntry] ], adjExternal : adjEntry, n : node = None) -> None:
		...

	def expandEdgePNode(self, spqrTree : StaticSPQRTree, treeNodeTreated : NodeArray[ bool ], mu : node, leftNode : node, nodeLength : NodeArray[ T ], edgeLength : NodeArray[EdgeArray[ T ] ], newOrder : NodeArray[List[adjEntry] ], adjBeforeNodeArraySource : NodeArray[ListIterator[adjEntry] ], adjBeforeNodeArrayTarget : NodeArray[ListIterator[adjEntry] ], adjExternal : adjEntry) -> None:
		...

	def expandEdgeRNode(self, spqrTree : StaticSPQRTree, treeNodeTreated : NodeArray[ bool ], mu : node, leftNode : node, nodeLength : NodeArray[ T ], edgeLength : NodeArray[EdgeArray[ T ] ], newOrder : NodeArray[List[adjEntry] ], adjBeforeNodeArraySource : NodeArray[ListIterator[adjEntry] ], adjBeforeNodeArrayTarget : NodeArray[ListIterator[adjEntry] ], adjExternal : adjEntry, n : node) -> None:
		...

	def expandEdgeSNode(self, spqrTree : StaticSPQRTree, treeNodeTreated : NodeArray[ bool ], mu : node, leftNode : node, nodeLength : NodeArray[ T ], edgeLength : NodeArray[EdgeArray[ T ] ], newOrder : NodeArray[List[adjEntry] ], adjBeforeNodeArraySource : NodeArray[ListIterator[adjEntry] ], adjBeforeNodeArrayTarget : NodeArray[ListIterator[adjEntry] ], adjExternal : adjEntry) -> None:
		...

	def largestFaceContainingNode(self, spqrTree : StaticSPQRTree, mu : node, n : node, nodeLength : NodeArray[ T ], edgeLength : NodeArray[EdgeArray[ T ] ]) -> T:
		"""Computes the size of a maximum face in the skeleton graph ofmucontainingn."""
		...

	def largestFaceInSkeleton(self, spqrTree : StaticSPQRTree, mu : node, nodeLength : NodeArray[ T ], edgeLength : NodeArray[EdgeArray[ T ] ]) -> T:
		"""Computes the size of a maximum face in the skeleton graph ofmu."""
		...

	def topDownTraversal(self, spqrTree : StaticSPQRTree, mu : node, nodeLength : NodeArray[ T ], edgeLength : NodeArray[EdgeArray[ T ] ]) -> None:
		"""Top down traversal of SPQR-tree computing the component length of all reference edges."""
		...
