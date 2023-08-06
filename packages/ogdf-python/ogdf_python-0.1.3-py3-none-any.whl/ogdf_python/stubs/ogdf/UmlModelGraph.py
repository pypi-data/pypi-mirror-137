# file stubs/ogdf/UmlModelGraph.py generated from classogdf_1_1_uml_model_graph
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
class UmlModelGraph(ogdf.Graph):

	"""This class represents the complete UML Model in a graph-like data structure."""

	def __init__(self) -> None:
		"""Constructor."""
		...

	def __destruct__(self) -> None:
		"""Destructor."""
		...

	def getNodeLabel(self, v : node) -> str:
		"""Returns a const reference to the label of the given node."""
		...

	def label(self, v : node) -> str:
		"""Returns a reference to the label of the given node."""
		...

	def setModelName(self, name : str) -> None:
		"""Sets the name of the model."""
		...

	@overload
	def type(self, e : edge) -> Graph.EdgeType:
		"""Returns a reference to the type of the given edge."""
		...

	@overload
	def type(self, e : edge) -> Graph.EdgeType:
		"""Returns a const reference to the type of the given edge."""
		...

	@overload
	def type(self, v : node) -> Graph.NodeType:
		"""Returns a reference to the type of the given node."""
		...

	@overload
	def type(self, v : node) -> Graph.NodeType:
		"""Returns a const reference to the type of the given node."""
		...
