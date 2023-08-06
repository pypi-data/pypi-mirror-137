# file stubs/ogdf/UmlDiagramGraph.py generated from classogdf_1_1_uml_diagram_graph
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
class UmlDiagramGraph(object):

	"""Contains the classUmlDiagramGraphwhich represents one particular diagram of the complete UML Model."""

	class UmlDiagramType(enum.Enum):

		"""This enum type represents the different diagram types of UML. */."""

		classDiagram = enum.auto()

		moduleDiagram = enum.auto()

		sequenceDiagram = enum.auto()

		collaborationDiagram = enum.auto()

		componentDiagram = enum.auto()

		unknownDiagram = enum.auto()

	def __init__(self, umlModelGraph : UmlModelGraph, diagramType : UmlDiagramType, diagramName : str) -> None:
		"""Constructor."""
		...

	def __destruct__(self) -> None:
		"""Destructor."""
		...

	def addEdge(self, umlEdge : edge) -> None:
		"""Adds an edge."""
		...

	def addNodeWithGeometry(self, umlNode : node, x : float, y : float, w : float, h : float) -> None:
		"""Adds a node with the given coordinates."""
		...

	def getDiagramName(self) -> str:
		"""Returns the name of the diagram."""
		...

	def getDiagramTypeString(self) -> str:
		"""Returns the type of the diagram as string."""
		...

	def getEdges(self) -> SList[edge]:
		"""Access to contained edges."""
		...

	def getHeight(self) -> SList[ float ]:
		"""Access to height."""
		...

	def getNodes(self) -> SList[node]:
		"""Access to contained nodes."""
		...

	def getWidth(self) -> SList[ float ]:
		"""Access to width."""
		...

	def getX(self) -> SList[ float ]:
		"""Access to x-coordinates."""
		...

	def getY(self) -> SList[ float ]:
		"""Access to y-coordinates."""
		...
