# file stubs/ogdf/internal/__init__.py generated from namespaceogdf_1_1internal
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
ArrayType = TypeVar('ArrayType')

GraphObjectPtr = TypeVar('GraphObjectPtr')

CONTAINER = TypeVar('CONTAINER')

ITERATOR = TypeVar('ITERATOR')

TYPE = TypeVar('TYPE')

class internal(object):

	GraphArrayConstIterator : Type = GraphArrayIteratorBase[ ArrayType, True ]

	GraphArrayIterator : Type = GraphArrayIteratorBase[ ArrayType, False ]

	GraphIterator : Type = GraphIteratorBase[ GraphObjectPtr, False ]

	GraphReverseIterator : Type = GraphIteratorBase[ GraphObjectPtr, True ]

	def chooseIteratorByFastTest(self, container : CONTAINER, includeElement : Callable) -> ITERATOR:
		...

	def chooseIteratorBySlowTest(self, container : CONTAINER, includeElement : Callable, size : int) -> ITERATOR:
		...

	def chooseIteratorFrom(self, container : CONTAINER, includeElement : Callable, isFastTest : bool) -> ITERATOR:
		"""Returns an iterator to a random element in thecontainer."""
		...

	@overload
	def getAllEdges(self, G : Graph, edges : Array[edge]) -> None:
		...

	@overload
	def getAllEdges(self, G : Graph, edges : CONTAINER) -> None:
		...

	@overload
	def getAllNodes(self, G : Graph, nodes : Array[node]) -> None:
		...

	@overload
	def getAllNodes(self, G : Graph, nodes : CONTAINER) -> None:
		...
