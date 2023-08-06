# file stubs/ogdf/ExtractKuratowskis.py generated from classogdf_1_1_extract_kuratowskis
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
class ExtractKuratowskis(object):

	"""Extracts multiple Kuratowski Subdivisions."""

	class KuratowskiType(enum.Enum):

		"""Enumeration over Kuratowski Type none, K33, K5."""

		#: no kuratowski subdivision exists
		none = enum.auto()

		#: a K3,3 subdivision exists
		K33 = enum.auto()

		#: a K5 subdivision exists
		K5 = enum.auto()

	#: Link to classBoyerMyrvoldPlanar.
	BMP : BoyerMyrvoldPlanar = ...

	#: The adjEntry which goes from DFS-parent to current vertex.
	m_adjParent : NodeArray[adjEntry] = ...

	#: Some parameters, seeBoyerMyrvoldfor further instructions.
	m_avoidE2Minors : bool = ...

	#: The one and only DFI-NodeArray.
	m_dfi : NodeArray[  int ] = ...

	#: Some parameters, seeBoyerMyrvoldfor further instructions.
	m_embeddingGrade : int = ...

	#: Input graph.
	m_g : Graph = ...

	#: Returns appropriate node from given DFI.
	m_nodeFromDFI : Array[node] = ...

	#: Value used as marker for visited nodes etc.
	m_nodeMarker : int = ...

	#: Arraymaintaining visited bits on each node.
	m_wasHere : NodeArray[  int ] = ...

	def __init__(self, bm : BoyerMyrvoldPlanar) -> None:
		"""Constructor."""
		...

	def __destruct__(self) -> None:
		"""Destructor."""
		...

	def extract(self, allKuratowskis : SListPure[KuratowskiStructure], output : SList[KuratowskiWrapper]) -> None:
		"""Extracts all Kuratowski Subdivisions and adds them tooutput(without bundles)"""
		...

	def extractBundles(self, allKuratowskis : SListPure[KuratowskiStructure], output : SList[KuratowskiWrapper]) -> None:
		"""Extracts all Kuratowski Subdivisions and adds them tooutput(with bundles)"""
		...

	def __assign__(self, _ : ExtractKuratowskis) -> ExtractKuratowskis:
		"""Assignment operator is undefined!"""
		...

	@overload
	def isANewKuratowski(self, test : EdgeArray[  int ], output : SList[KuratowskiWrapper]) -> bool:
		"""Returns true, iff the Kuratowski is not already contained in output."""
		...

	@overload
	def isANewKuratowski(self, g : Graph, kuratowski : SListPure[edge], output : SList[KuratowskiWrapper]) -> bool:
		"""Returns true, iff the Kuratowski is not already contained in output."""
		...

	def whichKuratowski(self, m_g : Graph, dfi : NodeArray[  int ], list : SListPure[edge]) -> KuratowskiType:
		"""Checks, iflistforms a valid Kuratowski Subdivision and returns the type."""
		...

	def whichKuratowskiArray(self, g : Graph, edgenumber : EdgeArray[  int ]) -> KuratowskiType:
		"""Checks, if edges inArrayedgenumberform a valid Kuratowski Subdivision and returns the type."""
		...

	def addDFSPath(self, list : SListPure[edge], bottom : node, top : node) -> None:
		"""Adds DFS-path from nodebottomto nodetoptolist."""
		...

	def addDFSPathReverse(self, list : SListPure[edge], bottom : node, top : node) -> None:
		"""Adds DFS-path from nodetopto nodebottomtolist."""
		...

	def addExternalFacePath(self, list : SListPure[edge], externPath : SListPure[adjEntry]) -> None:
		"""Adds external face edges tolist."""
		...

	def adjToLowestNodeBelow(self, high : node, low : int) -> adjEntry:
		"""ReturnsadjEntryof the edge between nodehighand a special node."""
		...

	def checkMinorE2(self, firstWPath : bool, firstWOnHighestXY : bool) -> bool:
		"""Checks for minortype E2 preconditions."""
		...

	def extractMinorA(self, output : SList[KuratowskiWrapper], k : KuratowskiStructure, pathX : SListPure[edge], endnodeX : node, pathY : SListPure[edge], endnodeY : node, pathW : SListPure[edge]) -> None:
		"""Extracts minortype A and adds it to listoutput."""
		...

	def extractMinorB(self, output : SList[KuratowskiWrapper], k : KuratowskiStructure, info : WInfo, pathX : SListPure[edge], endnodeX : node, pathY : SListPure[edge], endnodeY : node, pathW : SListPure[edge]) -> None:
		"""Extracts minortype B and adds it to listoutput(no bundles)"""
		...

	def extractMinorBBundles(self, output : SList[KuratowskiWrapper], nodeflags : NodeArray[  int ], nodemarker : int, k : KuratowskiStructure, flags : EdgeArray[  int ], info : WInfo, pathX : SListPure[edge], endnodeX : node, pathY : SListPure[edge], endnodeY : node, pathW : SListPure[edge]) -> None:
		"""Extracts minortype B and adds it to listoutput(with bundles)"""
		...

	def extractMinorC(self, output : SList[KuratowskiWrapper], k : KuratowskiStructure, info : WInfo, pathX : SListPure[edge], endnodeX : node, pathY : SListPure[edge], endnodeY : node, pathW : SListPure[edge]) -> None:
		"""Extracts minortype C and adds it to listoutput."""
		...

	def extractMinorD(self, output : SList[KuratowskiWrapper], k : KuratowskiStructure, info : WInfo, pathX : SListPure[edge], endnodeX : node, pathY : SListPure[edge], endnodeY : node, pathW : SListPure[edge]) -> None:
		"""Extracts minortype D and adds it to listoutput."""
		...

	def extractMinorE(self, output : SList[KuratowskiWrapper], firstXPath : bool, firstPath : bool, firstWPath : bool, firstWOnHighestXY : bool, k : KuratowskiStructure, info : WInfo, pathX : SListPure[edge], endnodeX : node, pathY : SListPure[edge], endnodeY : node, pathW : SListPure[edge]) -> None:
		"""Extracts minortype E and adds it to listoutput(no bundles)"""
		...

	def extractMinorE1(self, output : SList[KuratowskiWrapper], before : int, px : node, py : node, k : KuratowskiStructure, info : WInfo, pathX : SListPure[edge], endnodeX : node, pathY : SListPure[edge], endnodeY : node, pathW : SListPure[edge], pathZ : SListPure[edge], endnodeZ : node) -> None:
		"""Extracts minorsubtype E1 and adds it to listoutput."""
		...

	def extractMinorE2(self, output : SList[KuratowskiWrapper], k : KuratowskiStructure, info : WInfo, pathX : SListPure[edge], endnodeX : node, pathY : SListPure[edge], endnodeY : node, pathZ : SListPure[edge]) -> None:
		"""Extracts minorsubtype E2 and adds it to listoutput."""
		...

	def extractMinorE3(self, output : SList[KuratowskiWrapper], before : int, z : node, px : node, py : node, k : KuratowskiStructure, info : WInfo, pathX : SListPure[edge], endnodeX : node, pathY : SListPure[edge], endnodeY : node, pathW : SListPure[edge], pathZ : SListPure[edge], endnodeZ : node) -> None:
		"""Extracts minorsubtype E3 and adds it to listoutput."""
		...

	def extractMinorE4(self, output : SList[KuratowskiWrapper], before : int, z : node, px : node, py : node, k : KuratowskiStructure, info : WInfo, pathX : SListPure[edge], endnodeX : node, pathY : SListPure[edge], endnodeY : node, pathW : SListPure[edge], pathZ : SListPure[edge], endnodeZ : node) -> None:
		"""Extracts minorsubtype E4 and adds it to listoutput."""
		...

	def extractMinorE5(self, output : SList[KuratowskiWrapper], k : KuratowskiStructure, info : WInfo, pathX : SListPure[edge], endnodeX : node, pathY : SListPure[edge], endnodeY : node, pathW : SListPure[edge], pathZ : SListPure[edge], endnodeZ : node) -> None:
		"""Extracts minorsubtype E5 and adds it to listoutput."""
		...

	def extractMinorEBundles(self, output : SList[KuratowskiWrapper], firstXPath : bool, firstPath : bool, firstWPath : bool, firstWOnHighestXY : bool, nodeflags : NodeArray[  int ], nodemarker : int, k : KuratowskiStructure, flags : EdgeArray[  int ], info : WInfo, pathX : SListPure[edge], endnodeX : node, pathY : SListPure[edge], endnodeY : node, pathW : SListPure[edge]) -> None:
		"""Extracts minortype E and adds it to listoutput(bundles)"""
		...

	def isMinorE1(self, before : int, firstXPath : bool, firstYPath : bool) -> bool:
		"""Checks for minortype E1."""
		...

	def isMinorE2(self, endnodeX : node, endnodeY : node, endnodeZ : node) -> bool:
		"""Checks for minortype E2."""
		...

	def isMinorE3(self, endnodeX : node, endnodeY : node, endnodeZ : node) -> bool:
		"""Checks for minortype E3."""
		...

	def isMinorE4(self, px : node, py : node, k : KuratowskiStructure, info : WInfo) -> bool:
		"""Checks for minortype E4."""
		...

	def isMinorE5(self, px : node, py : node, k : KuratowskiStructure, endnodeX : node, endnodeY : node, endnodeZ : node) -> bool:
		"""Checks for minortype E5 (K5)"""
		...

	def truncateEdgelist(self, list1 : SListPure[edge], list2 : SListPure[edge]) -> None:
		"""Separateslist1from edges already contained inlist2."""
		...
