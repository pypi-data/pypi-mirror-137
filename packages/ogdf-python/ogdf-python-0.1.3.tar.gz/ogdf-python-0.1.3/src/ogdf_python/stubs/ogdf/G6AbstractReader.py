# file stubs/ogdf/G6AbstractReader.py generated from classogdf_1_1_g6_abstract_reader
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
Implementation = TypeVar('Implementation')

class G6AbstractReader(ogdf.G6AbstractInstance[ Implementation ], Generic[Implementation]):

	"""Abstract base class for readers."""

	class State(enum.Enum):

		"""Internal reader state."""

		#: Initial reader state.
		Start = enum.auto()

		#: Extra intermediary state to support graphs with a starting character.
		GraphStart = enum.auto()

		#: Header: size of graph encoded in multiple bytes.
		EighteenBit = enum.auto()

		#: Header: working state if we do have a multi-byte size.
		RemainingBits = enum.auto()

		#: Main graph body.
		Body = enum.auto()

	#: Whether we should be finished reading.
	m_finished : bool = ...

	#: Whether the currently read byte was the first for the graph body.
	m_firstByteInBody : bool = ...

	#: Whether we fail reading if no header was found.
	m_forceHeader : bool = ...

	m_G : Graph = ...

	#: Indices for every node.
	m_index : Array[node] = ...

	m_is : std.istream = ...

	#: Number of nodes as parsed from the input.
	m_numberOfNodes : int = ...

	#: Bit counter for header and Sparse6 parsing.
	m_remainingBits : int = ...

	#: Adjacency matrix source index. For Sparse6, this is the currently handled node.
	m_sourceIdx : int = ...

	m_state : State = ...

	#: Adjacency matrix target index. For Sparse6, this is the currently read information.
	m_targetIdx : int = ...

	def __init__(self, G : Graph, _is : std.istream, forceHeader : bool) -> None:
		...

	def good(self) -> bool:
		"""Returns true if the parsed number of nodes equal the number in the graph."""
		...

	def read(self) -> bool:
		"""Executes the read."""
		...

	def finalize(self) -> bool:
		"""Called after every byte of the body has been read."""
		...

	def init(self) -> None:
		"""Initializes a reader instance with proper starting values."""
		...

	def parseByteBody(self, byte : int) -> bool:
		"""Called for every read byte in the graph body."""
		...
