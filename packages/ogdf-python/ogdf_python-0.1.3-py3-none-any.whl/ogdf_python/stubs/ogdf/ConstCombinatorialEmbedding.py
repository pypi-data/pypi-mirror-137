# file stubs/ogdf/ConstCombinatorialEmbedding.py generated from classogdf_1_1_const_combinatorial_embedding
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
class ConstCombinatorialEmbedding(object):

	"""Combinatorial embeddings of planar graphs."""

	@overload
	def __init__(self) -> None:
		"""Creates a combinatorial embedding associated with no graph."""
		...

	@overload
	def __init__(self, G : Graph) -> None:
		"""Creates a combinatorial embedding of graphG."""
		...

	@overload
	def __init__(self, C : ConstCombinatorialEmbedding) -> None:
		"""Copy constructor."""
		...

	def __assign__(self, C : ConstCombinatorialEmbedding) -> ConstCombinatorialEmbedding:
		"""Assignment operator."""
		...

	def __destruct__(self) -> None:
		"""Destructor."""
		...

	def valid(self) -> bool:
		"""Returns whether the embedding is associated with a graph."""
		...

	def getGraph(self) -> Graph:
		"""Returns the associated graph of the combinatorial embedding."""
		...

	def __Graph__(self) -> None:
		"""Returns associated graph."""
		...

	def firstFace(self) -> face:
		"""Returns the first face in the list of all faces."""
		...

	def lastFace(self) -> face:
		"""Returns the last face in the list of all faces."""
		...

	def numberOfFaces(self) -> int:
		"""Returns the number of faces."""
		...

	def rightFace(self, adj : adjEntry) -> face:
		"""Returns the face to the right ofadj, i.e., the face containingadj."""
		...

	def leftFace(self, adj : adjEntry) -> face:
		"""Returns the face to the left ofadj, i.e., the face containing the twin ofadj."""
		...

	def maxFaceIndex(self) -> int:
		"""Returns the largest used face index."""
		...

	def faceArrayTableSize(self) -> int:
		"""Returns the table size of face arrays associated with this embedding."""
		...

	def chooseFace(self, includeFace : Callable = print, isFastTest : bool = True) -> face:
		"""Returns a random face."""
		...

	def maximalFace(self) -> face:
		"""Returns a face of maximal size."""
		...

	def externalFace(self) -> face:
		"""Returns the external face."""
		...

	def setExternalFace(self, f : face) -> None:
		"""Sets the external face tof."""
		...

	def isBridge(self, e : edge) -> bool:
		...

	@overload
	def init(self, G : Graph) -> None:
		"""Initializes the embedding for graphG."""
		...

	@overload
	def init(self) -> None:
		...

	def computeFaces(self) -> None:
		"""Computes the list of faces."""
		...

	def registerArray(self, pFaceArray : FaceArrayBase) -> ListIterator[FaceArrayBase]:
		"""Registers the face arraypFaceArray."""
		...

	def unregisterArray(self, it : ListIterator[FaceArrayBase]) -> None:
		"""Unregisters the face array identified byit."""
		...

	def moveRegisterArray(self, it : ListIterator[FaceArrayBase], pFaceArray : FaceArrayBase) -> None:
		"""Move the registrationitof a node array topFaceArray(used with move semantics for face arrays)."""
		...

	@overload
	def findCommonFace(self, v : node, w : node, left : bool = True) -> adjEntry:
		"""Identifies a common face of two nodes and returns the respective adjacency entry."""
		...

	@overload
	def findCommonFace(self, v : node, w : node, adjW : adjEntry, left : bool = True) -> adjEntry:
		"""Identifies a common face of two nodes and returns the respective adjacency entry."""
		...

	#: Provides a bidirectional iterator to a face in a combinatorial embedding.
	face_iterator : Type = internal.GraphIterator[face]

	#: The associated graph.
	m_cpGraph : Graph = ...

	m_externalFace : face = ...

	#: The current table size of face arrays.
	m_faceArrayTableSize : int = ...

	#: The index assigned to the next created face.
	m_faceIdCount : int = ...

	#: The critical section for protecting shared acces to register/unregister methods.
	m_mutexRegArrays : std.mutex = ...

	#: The external face.
	m_regFaceArrays : ListPure[FaceArrayBase] = ...

	#: The face to which an adjacency entry belongs.
	m_rightFace : AdjEntryArray[face] = ...

	#: The container containing all face objects.
	faces : internal.GraphObjectContainer[FaceElement] = ...

	def createFaceElement(self, adjFirst : adjEntry) -> face:
		"""Create a new face."""
		...

	def reinitArrays(self) -> None:
		"""Reinitialize associated face arrays."""
		...
