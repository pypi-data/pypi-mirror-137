# file stubs/ogdf/Prioritized.py generated from classogdf_1_1_prioritized
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
Priority = TypeVar('Priority')

X = TypeVar('X')

class Prioritized(Generic[X, Priority]):

	"""Augments any data elements of typeXwith keys of typePriority. This class is also its own Comparer."""

	@overload
	def __init__(self) -> None:
		"""Constructor of empty element. Be careful!"""
		...

	@overload
	def __init__(self, P : Prioritized) -> None:
		"""Copy-constructor."""
		...

	@overload
	def __init__(self, xt : X, pt : Priority) -> None:
		"""Constructor using a key/value pair."""
		...

	def item(self) -> X:
		"""Returns the data of the element."""
		...

	def __ne__(self, P : Prioritized[ X, Priority ]) -> bool:
		"""Comparison oprator based on the compare-operator for the key type (Priority)"""
		...

	def __lt__(self, P : Prioritized[ X, Priority ]) -> bool:
		"""Comparison oprator based on the compare-operator for the key type (Priority)"""
		...

	def __le__(self, P : Prioritized[ X, Priority ]) -> bool:
		"""Comparison oprator based on the compare-operator for the key type (Priority)"""
		...

	def __assign__(self, P : Prioritized[ X, Priority ]) -> Prioritized:
		"""Copy assignment operator."""
		...

	def __eq__(self, P : Prioritized[ X, Priority ]) -> bool:
		"""Comparison oprator based on the compare-operator for the key type (Priority)"""
		...

	def __gt__(self, P : Prioritized[ X, Priority ]) -> bool:
		"""Comparison oprator based on the compare-operator for the key type (Priority)"""
		...

	def __ge__(self, P : Prioritized[ X, Priority ]) -> bool:
		"""Comparison oprator based on the compare-operator for the key type (Priority)"""
		...

	def priority(self) -> Priority:
		"""Returns the key of the element."""
		...

	def setItem(self, item : X) -> None:
		"""Sets value x."""
		...

	def setPriority(self, pp : Priority) -> None:
		"""Sets priority."""
		...
