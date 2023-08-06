# file stubs/ogdf/steiner_tree/goemans/BlowupComponents.py generated from classogdf_1_1steiner__tree_1_1goemans_1_1_blowup_components
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
T = TypeVar('T')

class BlowupComponents(Generic[T]):

	"""Obtain and provides information about components in a given blowup graph."""

	componentCost : ArrayBuffer[ T ] = ...

	componentId : NodeArray[  int ] = ...

	componentRootEdge : ArrayBuffer[edge] = ...

	componentTerminals : ArrayBuffer[ArrayBuffer[node] ] = ...

	maxId : int = ...

	def initializeComponent(self, rootEdge : edge, blowupGraph : BlowupGraph[ T ]) -> None:
		"""Initialize all information about the component starting withrootEdgein the blowup graph."""
		...

	def __init__(self, blowupGraph : BlowupGraph[ T ]) -> None:
		"""Find all components in the blowup graph and initialize information them."""
		...

	def cost(self, id : int) -> T:
		"""Return total cost of a given component."""
		...

	def id(self, v : node) -> int:
		"""Return the component id a given node is contained in."""
		...

	def rootEdge(self, id : int) -> edge:
		"""Return the edge coming from the root of a given component."""
		...

	def setRootEdge(self, id : int, e : edge) -> None:
		"""Set the edge coming from the root for a given component."""
		...

	def size(self) -> int:
		"""Return number of components."""
		...

	def terminals(self, id : int) -> ArrayBuffer[node]:
		"""Return list of terminals for a given component."""
		...
