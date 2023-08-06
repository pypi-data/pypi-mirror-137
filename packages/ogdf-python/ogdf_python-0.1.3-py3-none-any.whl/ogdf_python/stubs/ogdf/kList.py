# file stubs/ogdf/kList.py generated from classogdf_1_1k_list
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
class kList(ogdf.List[ withKey ]):

	"""ClasskListextends the classListby functions needed in the FastHierarchLayout algorithm."""

	def add(self, e : int, k : float) -> None:
		...

	def median(self) -> float:
		...

	def peek(self) -> float:
		...

	def pop(self, e : int, k : float) -> bool:
		...

	def reduce(self, newList : kList) -> None:
		"""Scans the list for pairs of elements with the same double key."""
		...
