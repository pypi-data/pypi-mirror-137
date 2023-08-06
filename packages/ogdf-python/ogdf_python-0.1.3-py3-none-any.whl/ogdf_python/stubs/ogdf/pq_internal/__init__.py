# file stubs/ogdf/pq_internal/__init__.py generated from namespaceogdf_1_1pq__internal
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
C = TypeVar('C')

Impl = TypeVar('Impl')

P = TypeVar('P')

E = TypeVar('E')

class pq_internal(object):

	"""This namespace contains helper classes to keep the code dry."""

	#: Shortcut for the base class ofPrioritizedQueue.
	SuperQueueTemplate : Type = PriorityQueue[PairTemplate[ E, P ],Compare[PairTemplate[ E, P ], C ], Impl ]
