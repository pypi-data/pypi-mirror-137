# file stubs/ogdf/SubsetEnumerator.py generated from classogdf_1_1_subset_enumerator
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
ContainerType = TypeVar('ContainerType')

T = TypeVar('T')

class SubsetEnumerator(Generic[T]):

	"""Enumerator for k-subsets of a given type."""

	m_index : Array[  int ] = ...

	m_maxCard : int = ...

	m_subset : ArrayBuffer[ T ] = ...

	m_valid : bool = ...

	def initSubset(self, card : int) -> None:
		...

	def __init__(self, set : ContainerType) -> None:
		"""Constructor."""
		...

	def array(self, array : Array[ T ]) -> None:
		"""Obtains an array of the subset members."""
		...

	@overload
	def begin(self) -> None:
		"""Initializes theSubsetEnumeratorto enumerate all subsets."""
		...

	@overload
	def begin(self, card : int) -> None:
		"""Initializes theSubsetEnumeratorto enumerate subsets of given cardinality."""
		...

	@overload
	def begin(self, low : int, high : int) -> None:
		"""Initializes theSubsetEnumeratorto enumerate subsets of cardinalities from low to high."""
		...

	def forEachMember(self, func : Callable) -> None:
		"""Callsfuncfor each member in the subset."""
		...

	def forEachMemberAndNonmember(self, funcIn : Callable, funcNotIn : Callable) -> None:
		"""CallsfuncInfor each subset member andfuncNotInfor each other element of the set."""
		...

	def getSubsetAndComplement(self, subset : ContainerType, complement : ContainerType, func : Callable) -> None:
		"""Obtains a container of the subset members and a container of the other elements of the set."""
		...

	def hasMember(self, element : T) -> bool:
		"""Checks in O(subset cardinality) whetherelementis a member of the subset."""
		...

	@overload
	def list(self, subset : List[ T ]) -> None:
		"""Obtains (appends) a list of the subset members."""
		...

	@overload
	def list(self, subset : List[ T ], complement : List[ T ]) -> None:
		"""Obtains (appends) a list of the subset members and a list of the other elements of the set."""
		...

	def next(self) -> None:
		"""Obtains the next subset if possible. The result should be checked using thevalid()method."""
		...

	def numberOfMembersAndNonmembers(self) -> int:
		"""Returns the cardinality of the (super-)set. This is the maximum size that can be used for a subset."""
		...

	def __getitem__(self, i : int) -> T:
		"""Gets a member of subset by index (starting from 0)."""
		...

	def print(self, os : std.ostream, delim : str = " ") -> None:
		"""Prints subset to output streamosusing delimiterdelim."""
		...

	def size(self) -> int:
		"""Returns the cardinality of the subset."""
		...

	def testForAll(self, predicate : Callable) -> bool:
		"""Testspredicatefor all subset members."""
		...

	def valid(self) -> bool:
		"""Checks if the current subset is valid. If not, the subset is either not initialized or all subsets have already been enumerated."""
		...
