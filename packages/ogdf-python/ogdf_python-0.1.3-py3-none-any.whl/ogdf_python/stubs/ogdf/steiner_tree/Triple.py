# file stubs/ogdf/steiner_tree/Triple.py generated from classogdf_1_1steiner__tree_1_1_triple
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
T = TypeVar('T')

class Triple(Generic[T]):

	"""This class represents a triple used by various contraction-based minimum Steiner tree approximations."""

	def __init__(self, s0 : node = None, s1 : node = None, s2 : node = None, z : node = None, cost : T = 0, win : float = 0) -> None:
		...

	@overload
	def cost(self) -> T:
		...

	@overload
	def cost(self, c : T) -> None:
		...

	@overload
	def s0(self) -> node:
		...

	@overload
	def s0(self, u : node) -> None:
		...

	@overload
	def s1(self) -> node:
		...

	@overload
	def s1(self, u : node) -> None:
		...

	@overload
	def s2(self) -> node:
		...

	@overload
	def s2(self, u : node) -> None:
		...

	@overload
	def win(self) -> float:
		...

	@overload
	def win(self, w : float) -> None:
		...

	@overload
	def z(self) -> node:
		...

	@overload
	def z(self, u : node) -> None:
		...
