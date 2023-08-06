# file stubs/ogdf/FindKuratowskis.py generated from classogdf_1_1_find_kuratowskis
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
class FindKuratowskis(object):

	"""This class collects information about Kuratowski Subdivisions which is used for extraction later."""

	#: Listof all Kuratowski Structures.
	allKuratowskis : SListPure[KuratowskiStructure] = ...

	#: Current Kuratowski Structure.
	k : KuratowskiStructure = ...

	#: The adjEntry which goes from DFS-parent to current vertex.
	m_adjParent : NodeArray[adjEntry] = ...

	#: Holds information, if node is the source of a backedge.
	m_backedgeFlags : NodeArray[SListPure[adjEntry] ] = ...

	#: If true, bundles are extracted, otherwise single paths?
	m_bundles : bool = ...

	#: The one and only DFI-NodeArray.
	m_dfi : NodeArray[  int ] = ...

	#: Contains the type of each edge.
	m_edgeType : EdgeArray[BoyerMyrvoldEdgeType] = ...

	#: The embedding grade.
	m_embeddingGrade : int = ...

	#: Input graph.
	m_g : Graph = ...

	#: Links appropriateWInfoto node.
	m_getWInfo : NodeArray[WInfo] = ...

	#: The highest DFI in a subtree with node as root.
	m_highestSubtreeDFI : NodeArray[  int ] = ...

	#: The DFI of the least ancestor node over all backedges.
	m_leastAncestor : NodeArray[  int ] = ...

	#: The lowpoint of each node.
	m_lowPoint : NodeArray[  int ] = ...

	#: Returns appropriate node from given DFI.
	m_nodeFromDFI : Array[node] = ...

	#: Value used as marker for visited nodes etc.
	m_nodeMarker : int = ...

	#: Stores for each (virtual) bicomp root how many backedges to its bicomp still have to be embedded.
	m_numUnembeddedBackedgesInBicomp : NodeArray[  int ] = ...

	#: Listof virtual bicomp roots, that are pertinent to the current embedded node.
	m_pertinentRoots : NodeArray[SListPure[node] ] = ...

	#: Identifies the rootnode of the child bicomp the given backedge points to.
	m_pointsToRoot : EdgeArray[node] = ...

	#: Link to non-virtual vertex of a virtual Vertex.
	m_realVertex : NodeArray[node] = ...

	#: A list to all separated DFS-children of node.
	m_separatedDFSChildList : NodeArray[ListPure[node] ] = ...

	#: Arraymaintaining visited bits on each node.
	m_wasHere : NodeArray[  int ] = ...

	#: Link to classBoyerMyrvoldPlanar.
	pBM : BoyerMyrvoldPlanar = ...

	def __init__(self, bm : BoyerMyrvoldPlanar) -> None:
		"""Constructor."""
		...

	def __destruct__(self) -> None:
		"""Destructor."""
		...

	def addKuratowskiStructure(self, currentNode : node, root : node, stopx : node, stopy : node) -> None:
		"""Adds Kuratowski Structure on current node with rootrootand stopping nodesstopxandstopy."""
		...

	@overload
	def getAllKuratowskis(self) -> SListPure[KuratowskiStructure]:
		"""Get-method for the list of all KuratowskiStructures."""
		...

	@overload
	def getAllKuratowskis(self) -> SListPure[KuratowskiStructure]:
		"""Constant get-method for the list of all KuratowskiStructures."""
		...

	def __assign__(self, _ : FindKuratowskis) -> FindKuratowskis:
		...

	def extractExternalFacePath(self, externalFacePath : SListPure[adjEntry], highestFacePath : ArrayBuffer[adjEntry], marker : int, highMarker : int) -> None:
		"""Extracts externalFacePath in direction CCW and splits highestFacePath in highestXYPaths."""
		...

	def extractExternalSubgraph(self, stop : node, root : int, externalStartnodes : SListPure[  int ], externalEndnodes : SListPure[node]) -> None:
		"""Extracts external subgraph from nodestopto ancestors of node with DFIroot(without bundles)"""
		...

	def extractExternalSubgraphBundles(self, stop : node, root : int, externalSubgraph : SListPure[edge], nodeMarker : int) -> None:
		"""Extracts external subgraph from nodestopto ancestors of node with DFIroot(with bundles)"""
		...

	def extractHighestFacePath(self, highestFacePath : ArrayBuffer[adjEntry], marker : int) -> None:
		"""Extracts the highestFace Path of the bicomp containing both stopping nodes."""
		...

	def extractPertinentSubgraph(self, W_All : SListPure[WInfo]) -> None:
		"""Extracts pertinent subgraph from all wNodes toV(without bundles)"""
		...

	def extractPertinentSubgraphBundles(self, W_All : SListPure[WInfo], V : node, pertinentSubgraph : SListPure[edge], nodeMarker : int) -> None:
		"""Extracts pertinent subgraph from all wNodes toV(with bundles)"""
		...

	def findRoot(self, stopX : node) -> node:
		"""Finds root node of the bicomp containing the stopping nodestopX."""
		...

	def NodeArray(self, m_link) -> None:
		"""Links to opposite adjacency entries on external face in clockwise resp. ccw order."""
		...

	def splitInMinorTypes(self, externalFacePath : SListPure[adjEntry], marker : int) -> None:
		"""Assign pertinent nodes to the different minortypes and extracts inner externalPaths."""
		...
