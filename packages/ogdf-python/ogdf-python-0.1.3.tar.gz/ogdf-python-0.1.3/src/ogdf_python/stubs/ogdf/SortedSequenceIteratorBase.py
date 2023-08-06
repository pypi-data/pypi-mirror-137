# file stubs/ogdf/SortedSequenceIteratorBase.py generated from classogdf_1_1_sorted_sequence_iterator_base
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
# std::enable_if< isConst||!isArgConst, int >::type

isArgConst = TypeVar('isArgConst')

isArgReverse = TypeVar('isArgReverse')

isReverse = TypeVar('isReverse')

CMP = TypeVar('CMP')

isConst = TypeVar('isConst')

INFO = TypeVar('INFO')

KEY = TypeVar('KEY')

class SortedSequenceIteratorBase(Generic[KEY, INFO, CMP, isConst, isReverse]):

	"""Iterators for sorted sequences."""

	@overload
	def __init__(self) -> None:
		"""Creates an invalid (null-) iterator."""
		...

	@overload
	def __init__(self, it : SortedSequenceIteratorBase[ KEY, INFO, CMP, isArgConst, isArgReverse ]) -> None:
		"""Copy constructor."""
		...

	@overload
	def __init__(self, it : SortedSequenceIteratorBase[ KEY, INFO, CMP, isConst, isReverse ]) -> None:
		"""Copy constructor."""
		...

	def info(self) -> Union[INFO, INFO]:
		"""Returns the info of the sequence element pointed to."""
		...

	def key(self) -> KEY:
		"""Returns the key of the sequence element pointed to."""
		...

	def __ne__(self, it : SortedSequenceIteratorBase[ KEY, INFO, CMP, isConst, isReverse ]) -> bool:
		"""Inequality operator."""
		...

	def __preinc__(self) -> SortedSequenceIteratorBase[ KEY, INFO, CMP, isConst, isReverse ]:
		"""Move the iterator one item forward (prefix notation)"""
		...

	def __postinc__(self, _ : int) -> SortedSequenceIteratorBase[ KEY, INFO, CMP, isConst, isReverse ]:
		"""Moves the iterator one item forward (postfix notation)"""
		...

	def __predec__(self) -> SortedSequenceIteratorBase[ KEY, INFO, CMP, isConst, isReverse ]:
		"""Moves the iterator one item backward (prefix notation)"""
		...

	def __postdec__(self, _ : int) -> SortedSequenceIteratorBase[ KEY, INFO, CMP, isConst, isReverse ]:
		"""Moves the iterator one item backward (postfix notation)"""
		...

	def __assign__(self, it : SortedSequenceIteratorBase[ KEY, INFO, CMP, isConst, isReverse ]) -> SortedSequenceIteratorBase[ KEY, INFO, CMP, isConst, isReverse ]:
		"""Assignment operator."""
		...

	def __eq__(self, it : SortedSequenceIteratorBase[ KEY, INFO, CMP, isConst, isReverse ]) -> bool:
		"""Equality operator."""
		...

	def pred(self) -> SortedSequenceIteratorBase[ KEY, INFO, CMP, isConst, isReverse ]:
		"""Returns an iterator pointing to the previous element in the sequence."""
		...

	def succ(self) -> SortedSequenceIteratorBase[ KEY, INFO, CMP, isConst, isReverse ]:
		"""Returns an iterator pointing to the next element in the sequence."""
		...

	def valid(self) -> bool:
		"""Returns true if the iterator points to an element."""
		...
