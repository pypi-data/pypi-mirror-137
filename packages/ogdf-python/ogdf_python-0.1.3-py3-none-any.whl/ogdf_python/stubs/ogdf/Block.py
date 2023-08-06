# file stubs/ogdf/Block.py generated from classogdf_1_1_block
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
class Block(object):

	"""Class representing idea of Blocks used inGlobalSiftingandGridSiftingalgorithms."""

	@overload
	def __init__(self, e : edge) -> None:
		"""Creates new edge block for an edgee."""
		...

	@overload
	def __init__(self, v : node) -> None:
		"""Creates new vertex block for a nodev."""
		...

	def __destruct__(self) -> None:
		...

	def isEdgeBlock(self) -> bool:
		...

	def isVertexBlock(self) -> bool:
		...
