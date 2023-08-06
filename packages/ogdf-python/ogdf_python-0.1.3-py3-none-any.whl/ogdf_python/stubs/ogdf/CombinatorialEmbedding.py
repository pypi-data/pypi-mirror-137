# file stubs/ogdf/CombinatorialEmbedding.py generated from classogdf_1_1_combinatorial_embedding
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
class CombinatorialEmbedding(ogdf.ConstCombinatorialEmbedding):

	"""Combinatorial embeddings of planar graphs with modification functionality."""

	@overload
	def __init__(self) -> None:
		"""Creates a combinatorial embedding associated with no graph."""
		...

	@overload
	def __init__(self, G : Graph) -> None:
		"""Creates a combinatorial embedding of graphG."""
		...

	# Access to the associated graph

	@overload
	def getGraph(self) -> Graph:
		"""Returns the associated graph."""
		...

	@overload
	def getGraph(self) -> Graph:
		...

	@overload
	def __Graph__(self) -> None:
		...

	@overload
	def __Graph__(self) -> None:
		...

	# Initialization

	def init(self, G : Graph) -> None:
		"""Initializes the embedding for graphG."""
		...

	def clear(self) -> None:
		"""Removes all nodes, edges, and faces from the graph and the embedding."""
		...

	# Update of embedding

	def split(self, e : edge) -> edge:
		"""Splits edgee=(v,w) intoe=(v,u) ande'=(u,w) creating a new nodeu."""
		...

	def unsplit(self, eIn : edge, eOut : edge) -> None:
		"""Undoes a split operation."""
		...

	def splitNode(self, adjStartLeft : adjEntry, adjStartRight : adjEntry) -> node:
		"""Splits a node while preserving the order of adjacency entries."""
		...

	def contract(self, e : edge) -> node:
		"""Contracts edgee."""
		...

	def splitFace(self, adjSrc : adjEntry, adjTgt : adjEntry) -> edge:
		"""Splits a face by inserting a new edge."""
		...

	@overload
	def addEdgeToIsolatedNode(self, v : node, adjTgt : adjEntry) -> edge:
		"""Inserts a new edge similarly tosplitFacewithout having to callcomputeFacesagain."""
		...

	@overload
	def addEdgeToIsolatedNode(self, adjSrc : adjEntry, v : node) -> edge:
		"""Inserts a new edge similarly tosplitFacewithout having to callcomputeFacesagain."""
		...

	def joinFaces(self, e : edge) -> face:
		"""Removes edgeeand joins the two faces adjacent toe."""
		...

	def reverseEdge(self, e : edge) -> None:
		"""Reverses edgeseand updates embedding."""
		...

	def moveBridge(self, adjBridge : adjEntry, adjBefore : adjEntry) -> None:
		"""Moves a bridge in the graph."""
		...

	def removeDeg1(self, v : node) -> None:
		"""Removes degree-1 nodev."""
		...

	def updateMerger(self, e : edge, fRight : face, fLeft : face) -> None:
		"""Update face information after inserting a merger in a copy graph."""
		...

	def joinFacesPure(self, e : edge) -> face:
		"""Joins the two faces adjacent toebut does not remove edgee."""
		...
