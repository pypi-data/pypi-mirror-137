# file stubs/ogdf/BoyerMyrvoldPlanar.py generated from classogdf_1_1_boyer_myrvold_planar
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
class BoyerMyrvoldPlanar(object):

	"""This class implements the extendedBoyerMyrvoldplanarity embedding algorithm."""

	# Methods for Walkup and Walkdown

	def pertinent(self, w : node) -> bool:
		"""Checks whether nodewis pertinent.whas to be non-virtual."""
		...

	def internallyActive(self, w : node, v : int) -> bool:
		"""Checks whether real nodewis internally active while embedding node with DFIv."""
		...

	def externallyActive(self, w : node, v : int) -> bool:
		"""Checks whether real nodewis externally active while embedding node with DFIv."""
		...

	def inactive(self, w : node, v : int) -> bool:
		"""Checks whether real nodewis inactive while embedding node with DFIv."""
		...

	def infoAboutNode(self, w : node, v : int) -> int:
		"""Checks all dynamic information about a nodewwhile embedding node with DFIv."""
		...

	def successorOnExternalFace(self, w : node, direction : int) -> node:
		"""Walks upon external face in the givendirectionstarting atw."""
		...

	def successorWithoutShortCircuit(self, w : node, direction : int) -> node:
		"""Walks upon external face in givendirectionavoiding short circuit edges."""
		...

	def constSuccessorOnExternalFace(self, v : node, direction : int) -> node:
		"""Returns the successornode on the external face in givendirection."""
		...

	def constSuccessorWithoutShortCircuit(self, v : node, direction : int) -> node:
		"""Walks upon external face indirectionavoiding short circuit edges."""
		...

	def beforeShortCircuitEdge(self, v : node, direction : int) -> adjEntry:
		"""Returns underlying former adjEntry, if a short circuit edge indirectionofvexists."""
		...

	def activeSuccessor(self, w : node, direction : int, v : int, info : int) -> node:
		"""Walks upon external face in the givendirectionstarting atwuntil an active vertex is reached."""
		...

	def constActiveSuccessor(self, w : node, direction : int, v : int, info : int) -> node:
		"""Walks upon external face in the givendirection(without changing it) until an active vertex is reached."""
		...

	def wNodesExist(self, root : node, stopx : node, stopy : node) -> bool:
		"""Checks, if one ore more wNodes exist between the two stopping verticesstopxandstopy."""
		...

	def printNodeInfo(self, v : node) -> None:
		"""Prints informations about nodev."""
		...

	def mergeBiconnectedComponent(self, stack : ArrayBuffer[  int ]) -> None:
		"""Merges the last two biconnected components saved instack. Embeds them iffm_embeddingGrade!=EmbeddingGrade::doNotEmbed."""
		...

	def embedBackedges(self, v : node, v_dir : int, w : node, w_dir : int) -> None:
		"""Links (and embeds iffm_embeddingGrade!=EmbeddingGrade::doNotEmbed) backedges from nodevwith directionv_dirto nodewwith directionw_dir."""
		...

	def createShortCircuitEdge(self, v : node, v_dir : int, w : node, w_dir : int) -> None:
		"""Creates a short circuit edge from nodevwith directionv_dirto nodewwith directionw_dir."""
		...

	def walkup(self, v : node, w : node, marker : int, back : edge) -> node:
		"""Walkup: Builds the pertinent subgraph for the backedgeback."""
		...

	def walkdown(self, i : int, v : node, findKuratowskis : FindKuratowskis) -> int:
		"""Walkdown: Embeds all backedges with DFIias targetnode to nodev."""
		...

	def mergeUnprocessedNodes(self) -> None:
		"""Merges unprocessed virtual nodes such as the dfs-roots with their real counterpart."""
		...

	def postProcessEmbedding(self) -> None:
		"""Postprocessing of the graph, so that all virtual vertices are embedded and all bicomps are flipped."""
		...

	def embed(self) -> bool:
		"""Starts the embedding phase, which embedsm_gnode by node in descending DFI-order."""
		...

	# Some parameters... see BoyerMyrvold for further options

	m_bundles : bool = ...

	m_embeddingGrade : int = ...

	m_limitStructures : bool = ...

	m_randomness : float = ...

	m_avoidE2Minors : bool = ...

	m_edgeCosts : EdgeArray[  int ] = ...

	m_rand : std.minstd_rand = ...

	# Members from BoyerMyrvoldInit

	#: Link to non-virtual vertex of a virtual Vertex.
	m_realVertex : NodeArray[node] = ...

	#: The one and only DFI-NodeArray.
	m_dfi : NodeArray[  int ] = ...

	#: Returns appropriate node from given DFI.
	m_nodeFromDFI : Array[node] = ...

	#: Links to opposite adjacency entries on external face in clockwise resp. ccw order.
	m_link : NodeArray[adjEntry] = ...

	#: Links for short circuit edges.
	m_beforeSCE : NodeArray[adjEntry] = ...

	#: The adjEntry which goes from DFS-parent to current vertex.
	m_adjParent : NodeArray[adjEntry] = ...

	#: The DFI of the least ancestor node over all backedges.
	m_leastAncestor : NodeArray[  int ] = ...

	#: Contains the type of each edge.
	m_edgeType : EdgeArray[BoyerMyrvoldEdgeType] = ...

	#: The lowpoint of each node.
	m_lowPoint : NodeArray[  int ] = ...

	#: The highest DFI in a subtree with node as root.
	m_highestSubtreeDFI : NodeArray[  int ] = ...

	#: A list to all separated DFS-children of node.
	m_separatedDFSChildList : NodeArray[ListPure[node] ] = ...

	#: Pointer to node contained in the DFSChildList of his parent, if exists.
	m_pNodeInParent : NodeArray[ListIterator[node] ] = ...

	# Members for Walkup and Walkdown

	#: ThisArraykeeps track of all vertices that are visited by current walkup.
	m_visited : NodeArray[  int ] = ...

	#: Identifies the rootnode of the child bicomp the given backedge points to.
	m_pointsToRoot : EdgeArray[node] = ...

	#: Stores for each (real) non-root vertex v with which backedge it was visited during the walkup.
	m_visitedWithBackedge : NodeArray[edge] = ...

	#: Stores for each (virtual) bicomp root how many backedges to its bicomp still have to be embedded.
	m_numUnembeddedBackedgesInBicomp : NodeArray[  int ] = ...

	#: Iff true, the node is the root of a bicomp which has to be flipped.
	m_flipped : NodeArray[ bool ] = ...

	#: Holds information, if node is the source of a backedge.
	m_backedgeFlags : NodeArray[SListPure[adjEntry] ] = ...

	#: Listof virtual bicomp roots, that are pertinent to the current embedded node.
	m_pertinentRoots : NodeArray[SListPure[node] ] = ...

	#: Data structure for the Kuratowski subdivisions, which will be returned.
	m_output : SListPure[KuratowskiStructure] = ...

	class EmbeddingGrade(enum.Enum):

		"""Denotes the different embedding options."""

		doNotEmbed = enum.auto()

		doNotFind = enum.auto()

		doFindUnlimited = enum.auto()

		doFindZero = enum.auto()

	#: Direction for counterclockwise traversal.
	DirectionCCW : int = ...

	#: Direction for clockwise traversal.
	DirectionCW : int = ...

	#: Flag for extracting a planar subgraph instead of testing for planarity.
	m_extractSubgraph : bool = ...

	#: The whole number of bicomps, which have to be flipped.
	m_flippedNodes : int = ...

	#: Input graph, which can be altered.
	m_g : Graph = ...

	@overload
	def __init__(self, g : Graph, bundles : bool, embeddingGrade : EmbeddingGrade, limitStructures : bool, output : SListPure[KuratowskiStructure], randomness : float, avoidE2Minors : bool, extractSubgraph : bool, edgeCosts : EdgeArray[  int ] = None) -> None:
		"""Constructor, for parameters seeBoyerMyrvold."""
		...

	@overload
	def __init__(self, g : Graph, bundles : bool, embeddingGrade : int, limitStructures : bool, output : SListPure[KuratowskiStructure], randomness : float, avoidE2Minors : bool, extractSubgraph : bool, edgeCosts : EdgeArray[  int ] = None) -> None:
		"""Constructor, for parameters seeBoyerMyrvold."""
		...

	def flipBicomp(self, c : int, marker : int, visited : NodeArray[  int ], wholeGraph : bool, deleteFlipFlags : bool) -> None:
		"""Flips all nodes of the bicomp with unique, real, rootchild c as necessary."""
		...

	def __assign__(self, _ : BoyerMyrvoldPlanar) -> BoyerMyrvoldPlanar:
		"""Assignment operator is undefined!"""
		...

	def seed(self, rand : std.minstd_rand) -> None:
		"""Seeds the random generator for performing a random DFS. If this method is never called the random generator will be seeded by a value extracted from the global random generator."""
		...

	def start(self) -> bool:
		"""Starts the embedding algorithm."""
		...
