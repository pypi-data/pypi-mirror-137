# file stubs/ogdf/NonPlanarCore/__init__.py generated from classogdf_1_1_non_planar_core
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
TCost = TypeVar('TCost')

class NonPlanarCore(Generic[TCost]):

	"""Non-planar core reduction."""

	#: Costs to cross each edge of the core.
	m_cost : EdgeArray[ TCost ] = ...

	#: A pointer to a copy of the original graph, in which crossings are replaced by dummy nodes.
	m_endGraph : GraphCopy = ...

	#: The core.
	m_graph : Graph = ...

	#: The mapping between the edges of each embedding and their original.
	m_mapE : EdgeArray[EdgeArray[edge]  ] = ...

	#: The mapping between the nodes of each embedding and their original.
	m_mapV : EdgeArray[NodeArray[node]  ] = ...

	#: Traversing path for an edge in the core.
	m_mincut : EdgeArray[List[CutEdge] ] = ...

	#: Corresp. original node.
	m_orig : NodeArray[node] = ...

	#: A pointer to a copy of the core, in which crossings are replaced by dummy nodes.
	m_planarCore : GraphCopy = ...

	#: The original graph.
	m_pOriginal : Graph = ...

	#: Corresp. original edge (0 if virtual)
	m_real : EdgeArray[edge] = ...

	#: The s node of the st-component of a core edge.
	m_sNode : EdgeArray[node] = ...

	#: TheSPQRTreethat represents the original graph.
	m_T : StaticSPQRTree = ...

	#: The t node of the st-component of a core edge.
	m_tNode : EdgeArray[node] = ...

	#: The graph for the underlying skeleton of a virtual edge in the core.
	m_underlyingGraphs : EdgeArray[Graph] = ...

	@overload
	def __init__(self, G : Graph, nonPlanarityGuaranteed : bool = False) -> None:
		"""The unweighted version of the Algorithm call and constructor."""
		...

	@overload
	def __init__(self, G : Graph, weight : EdgeArray[ TCost ], nonPlanarityGuaranteed : bool = False) -> None:
		"""An slimmed version of the Algorithm call and constructor."""
		...

	@overload
	def __init__(self, G : Graph, weight : EdgeArray[ TCost ], minSTCutModule : MinSTCutModule[ TCost ], nonPlanarityGuaranteed : bool = False) -> None:
		"""Algorithm call and constructor."""
		...

	def __destruct__(self) -> None:
		...

	def core(self) -> Graph:
		"""Returns the non-planar core."""
		...

	@overload
	def cost(self) -> EdgeArray[ TCost ]:
		"""Returns the costs of the edges in the core, which is the number of original edges crossed, ifeis crossed, i.e."""
		...

	@overload
	def cost(self, e : edge) -> TCost:
		"""Returns the cost ofe, which is the number of original edges crossed, ifeis crossed, i.e."""
		...

	def isVirtual(self, e : edge) -> bool:
		"""True iff the edgeein the core represents more than one orginal edge and therefore is virtual."""
		...

	def mapE(self, e : edge) -> EdgeArray[edge]:
		"""Returns a map from the edges of the st-component represented by the core edge e to the original graph."""
		...

	def mincut(self, e : edge) -> List[CutEdge]:
		"""Returns the mincut of the st-component represented bye."""
		...

	@overload
	def original(self, e : edge) -> List[edge]:
		"""Returns the edges of the original graph, which are represented byein the core."""
		...

	@overload
	def original(self, v : node) -> node:
		"""Returns the node of the original graph, which is represented byvin the core."""
		...

	def originalGraph(self) -> Graph:
		"""Returns the original graph."""
		...

	def realEdge(self, e : edge) -> edge:
		"""Returns the edge of the orginal graph, which is represented byeor nullptr iffeis virtual."""
		...

	def retransform(self, planarCore : GraphCopy, planarGraph : GraphCopy, pCisPlanar : bool = True) -> None:
		"""Inserts the crossings from a copy of the core into a copy of the original graph."""
		...

	def sNode(self, e : edge) -> node:
		"""Returns the s node of the skeleton of the st-component represented by the core edgee= (s,t) Note that this node is not contained in the input graph, but an internal auxiliary graph."""
		...

	def tNode(self, e : edge) -> node:
		"""Returns the t node of the skeleton of the st-component represented by the core edgee= (s,t) Note that this node is not contained in the input graph, but an internal auxiliary graph."""
		...

	def call(self, G : Graph, weight : EdgeArray[ TCost ], minSTCutModule : MinSTCutModule[ TCost ], nonPlanarityGuaranteed : bool) -> None:
		"""The private method behind the constructors."""
		...

	def getAllMultiedges(self, winningEdges : List[edge], losingEdges : List[edge]) -> None:
		"""Checks for multiedges in the core."""
		...

	def getMincut(self, e : edge, cut : List[edge]) -> None:
		"""Get the mincut ofewith respect to its position in the chain of its original edge."""
		...

	def glue(self, eWinner : edge, eLoser : edge) -> None:
		"""Glues together the skeletons ofeWinnerandeLoserfor pruned P- and S-nodes."""
		...

	def glueMincuts(self, eWinner : edge, eLoser : edge) -> None:
		"""Glues together the mincuts of the winner and the loser edge."""
		...

	def importEmbedding(self, e : edge) -> None:
		"""This method asserts that all parts of the end graph that are represented by edgeeinternally have the same embedding every time retransform is called, regardless of which planarization of the core is given."""
		...

	def inflateCrossing(self, v : node) -> None:
		"""The crossing denoted by dummy nodevfrom the planarized copy of the core get inserted into the end graph."""
		...

	def markCore(self, mark : NodeArray[ bool ]) -> None:
		"""Marks all nodes of the underlyingSPQRTreeand prunes planar leaves until the marked nodes span a tree, which has only non-planar leaves, i.e."""
		...

	def normalizeCutEdgeDirection(self, coreEdge : edge) -> None:
		"""Every edge ofcoreEdge'scut that doesn't go the same direction ascoreEdgegets reversed."""
		...

	def removeSplitdummies(self, splitdummies : List[node]) -> None:
		"""After inserting the crossings, the end graph edges don't need to be partitioned anymore so thesplitdummiesget removed."""
		...

	def splitEdgeIntoSections(self, e : edge, splitdummies : List[node]) -> None:
		"""To be able to insert crossings correctly, an end graph edge ought to be split into n-1 sections if n is the number of crossings on the edge."""
		...

	def traversingPath(self, Sv : Skeleton, eS : edge, path : List[CutEdge], mapV : NodeArray[node], coreEdge : edge, weight_src : EdgeArray[ TCost ], minSTCutModule : MinSTCutModule[ TCost ]) -> None:
		"""Computes the traversing path for a given edge and the unmarked tree rooted in the node ofeSand saves the combinatorial embedding of the st-component whicheSrepresents, i.e."""
		...
