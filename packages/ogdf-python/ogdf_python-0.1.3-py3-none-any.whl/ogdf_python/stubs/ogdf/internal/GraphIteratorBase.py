# file stubs/ogdf/internal/GraphIteratorBase.py generated from classogdf_1_1internal_1_1_graph_iterator_base
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
GraphObjectPtr = TypeVar('GraphObjectPtr')

isReverse = TypeVar('isReverse')

isArgReverse = TypeVar('isArgReverse')

class GraphIteratorBase(Generic[GraphObjectPtr, isReverse]):

	@overload
	def __init__(self) -> None:
		...

	@overload
	def __init__(self, it : GraphIteratorBase[ GraphObjectPtr, isArgReverse ]) -> None:
		...

	@overload
	def __init__(self, ptr : GraphObjectPtr) -> None:
		...

	def __ne__(self, other : GraphIteratorBase[ GraphObjectPtr, isReverse ]) -> bool:
		...

	def __deref__(self) -> GraphObjectPtr:
		...

	def __preinc__(self) -> GraphIteratorBase[ GraphObjectPtr, isReverse ]:
		"""Increment operator (prefix)."""
		...

	def __postinc__(self, _ : int) -> GraphIteratorBase[ GraphObjectPtr, isReverse ]:
		"""Increment operator (postfix)."""
		...

	def __predec__(self) -> GraphIteratorBase[ GraphObjectPtr, isReverse ]:
		"""Decrement operator (prefix)."""
		...

	def __postdec__(self, _ : int) -> GraphIteratorBase[ GraphObjectPtr, isReverse ]:
		"""Decrement operator (postfix)."""
		...

	def __eq__(self, other : GraphIteratorBase[ GraphObjectPtr, isReverse ]) -> bool:
		...
