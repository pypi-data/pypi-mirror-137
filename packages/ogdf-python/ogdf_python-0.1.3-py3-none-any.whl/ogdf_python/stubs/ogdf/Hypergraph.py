# file stubs/ogdf/Hypergraph.py generated from classogdf_1_1_hypergraph
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
LIST = TypeVar('LIST')

class Hypergraph(object):

	OGDF_MALLOC_NEW_DELETE = ...

	@overload
	def __init__(self) -> None:
		"""Constructs an empty hypergraph."""
		...

	@overload
	def __init__(self, H : Hypergraph) -> None:
		"""Constructs a hypergraph that is a copy ofH."""
		...

	def __destruct__(self) -> None:
		"""Destructor."""
		...

	def allHyperedges(self, hyperedgeList : LIST) -> None:
		"""Returns a list with all hyperedges of the hypergraph."""
		...

	def allHypernodes(self, hypernodeList : LIST) -> None:
		"""Returns a list with all hypernodes of the hypergraph."""
		...

	def clear(self) -> None:
		"""Removes all hypernodes and all hyperedges from the hypergraph."""
		...

	def consistency(self) -> bool:
		"""Checks the consistency of the data structure."""
		...

	def delHyperedge(self, e : hyperedge) -> None:
		"""Removes hyperedgeefrom the hypergraph."""
		...

	def delHypernode(self, v : hypernode) -> None:
		"""Removes hypernodevand all incident hyperedges from the hypergraph."""
		...

	def empty(self) -> bool:
		"""Returns true iff the hypergraph is empty (ie. contains no hypernodes)."""
		...

	def firstHyperedge(self) -> hyperedge:
		"""Returns the first hyperedge in the list of all hyperedges."""
		...

	def firstHypernode(self) -> hypernode:
		"""Returns the first hypernode in the list of all hypernodes."""
		...

	def hyperedgeArrayTableSize(self) -> int:
		"""Returns the table size of hyperedge arrays within the hypergraph."""
		...

	def hyperedges(self) -> internal.GraphList[HyperedgeElement]:
		"""Returns the list of all hyperedges."""
		...

	def hypernodeArrayTableSize(self) -> int:
		"""Returns the table size of hypernode arrays with the hypergraph."""
		...

	def hypernodes(self) -> internal.GraphList[HypernodeElement]:
		"""Returns the list of all hypernodes."""
		...

	def lastHyperEdge(self) -> hyperedge:
		"""Returns the last hyperedge in the list of all hyperedges."""
		...

	def lastHypernode(self) -> hypernode:
		"""Returns the last hypernode in the list of all hypernodes."""
		...

	def loadPlaHypergraph(self, fileName : str) -> None:
		"""Reads hypergraph in pla format from the file."""
		...

	def maxHyperedgeIndex(self) -> int:
		"""Returns the largest used hyperedge index."""
		...

	def maxHypernodeIndex(self) -> int:
		"""Returns the largest used hypernode index."""
		...

	@overload
	def newHyperedge(self, pIndex : int, hypernodes : List[hypernode]) -> hyperedge:
		"""Creates a new hyperedge betweenhypernodesand returns it."""
		...

	@overload
	def newHyperedge(self, hypernodes : List[hypernode]) -> hyperedge:
		"""Creates a new hyperedge btweenhypernodesand returns it."""
		...

	@overload
	def newHypernode(self) -> hypernode:
		"""Creates a new hypernode and returns it."""
		...

	@overload
	def newHypernode(self, pType : HypernodeElement.Type) -> hypernode:
		"""Creates a new hypernode with givenpTypeand returns it."""
		...

	@overload
	def newHypernode(self, pIndex : int) -> hypernode:
		"""Creates a new hypernode with givenpIndexand returns it."""
		...

	@overload
	def newHypernode(self, pIndex : int, pType : HypernodeElement.Type) -> hypernode:
		"""Creates a new hypernode with givenpIndexandpTypeand returns it."""
		...

	def numberOfHyperedges(self) -> int:
		"""Returns the number of hyperedges in the hypergraph."""
		...

	def numberOfHypernodes(self) -> int:
		"""Returns the number of hypernodes in the hypergraph."""
		...

	def __assign__(self, H : Hypergraph) -> Hypergraph:
		...

	def randomHyperedge(self) -> hyperedge:
		"""Returns a randomly chosen hyperedge."""
		...

	def randomHypernode(self) -> hypernode:
		"""Returns a randomly chosen hypergraph."""
		...

	@overload
	def readBenchHypergraph(self, filename : str) -> None:
		"""Reads hypergraph in bench format from the file."""
		...

	@overload
	def readBenchHypergraph(self, _is : std.istream) -> None:
		"""Reads hypergraph in bench format from the input stream."""
		...

	def readPlaHypergraph(self, _is : std.istream) -> None:
		"""Reads hypergraph in pla format from the input stream."""
		...

	def registerHyperedgeArray(self, pHyperedgeArray : HypergraphArrayBase) -> ListIterator[HypergraphArrayBase]:
		...

	def registerHypernodeArray(self, pHypernodeArray : HypergraphArrayBase) -> ListIterator[HypergraphArrayBase]:
		"""Registers a node array."""
		...

	def registerObserver(self, pObserver : HypergraphObserver) -> ListIterator[HypergraphObserver]:
		"""Registers a hypergraph observer (e.g. aEdgeStandardRep)."""
		...

	def unregisterHyperedgeArray(self, it : ListIterator[HypergraphArrayBase]) -> None:
		"""Unregisters an hyperedge array."""
		...

	def unregisterHypernodeArray(self, it : ListIterator[HypergraphArrayBase]) -> None:
		"""Unregisters a hypernode array."""
		...

	def unregisterObserver(self, it : ListIterator[HypergraphObserver]) -> None:
		"""Unregisters a hypergraph observer."""
		...
