# file stubs/ogdf/internal/GraphObjectContainer.py generated from classogdf_1_1internal_1_1_graph_object_container
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
GraphObject = TypeVar('GraphObject')

class GraphObjectContainer(ogdf.internal.GraphList[ GraphObject ], Generic[GraphObject]):

	#: Provides a bidirectional iterator to an object in the container.
	iterator : Type = GraphIterator[ GraphObject  ]

	#: Provides a bidirectional reverse iterator to an object in the container.
	reverse_iterator : Type = GraphReverseIterator[ GraphObject  ]

	#: The value type (a pointer to a specific graph object)
	value_type : Type = GraphObject

	def begin(self) -> iterator:
		"""Returns an iterator to the first element in the container."""
		...

	def end(self) -> iterator:
		"""Returns an iterator to the one-past-last element in the container."""
		...

	def rbegin(self) -> reverse_iterator:
		"""Returns a reverse iterator to the last element in the container."""
		...

	def rend(self) -> reverse_iterator:
		"""Returns a reverse iterator to the one-before-first element in the container."""
		...
