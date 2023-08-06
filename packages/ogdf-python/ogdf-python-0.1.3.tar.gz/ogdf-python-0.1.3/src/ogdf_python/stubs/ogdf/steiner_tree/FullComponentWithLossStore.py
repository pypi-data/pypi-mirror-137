# file stubs/ogdf/steiner_tree/FullComponentWithLossStore.py generated from classogdf_1_1steiner__tree_1_1_full_component_with_loss_store
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
T = TypeVar('T')

class FullComponentWithLossStore(ogdf.steiner_tree.FullComponentWithExtraStore[ T, LossMetadata[ T ] ], Generic[T]):

	"""A data structure to store full components with additional "loss" functionality."""

	#: Indicates which Steiner node is connected to which terminal through the loss edges, indexed by the Steiner node.
	m_lossTerminal : NodeArray[node] = ...

	def findLossTerminal(self, u : node, pred : NodeArray[edge]) -> node:
		"""Starting from a Steiner node find the nearest terminal along a shortest path."""
		...

	def computeAllLosses(self) -> None:
		"""Compute the loss, both edge set and value, of all full components."""
		...

	def loss(self, id : int) -> T:
		"""Returns the loss value of full component with given id."""
		...

	def lossBridges(self, id : int) -> List[edge]:
		"""Returns a list of non-loss edges (that are bridges between the Loss components) of full component with given id."""
		...

	def lossTerminal(self, v : node) -> node:
		"""Returns the terminal (in the original graph) that belongs to a given node v (in the store) according to the Loss of the component."""
		...
