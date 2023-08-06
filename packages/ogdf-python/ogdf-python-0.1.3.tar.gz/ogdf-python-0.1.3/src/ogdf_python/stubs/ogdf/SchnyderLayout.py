# file stubs/ogdf/SchnyderLayout.py generated from classogdf_1_1_schnyder_layout
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
class SchnyderLayout(ogdf.PlanarGridLayoutModule):

	"""The classSchnyderLayoutrepresents the layout algorithm by Schnyder [Sch90]."""

	class CombinatorialObjects(enum.Enum):

		"""Each node in a Schnyder wood splits the graph into three regions."""

		#: Count the number of vertices in each region i and subtract the depth of the (i-1)-path of the node.
		VerticesMinusDepth = enum.auto()

		#: Count the number of faces in each region i.
		Faces = enum.auto()

	def __init__(self) -> None:
		...

	def getCombinatorialObjects(self) -> CombinatorialObjects:
		"""Returns the type of combinatorial objects whose number corresponds to the node coordinates."""
		...

	def setCombinatorialObjects(self, combinatorialObjects : CombinatorialObjects) -> None:
		"""Sets the type of combinatorial objects whose number corresponds to the node coordinates."""
		...

	def doCall(self, G : Graph, adjExternal : adjEntry, gridLayout : GridLayout, boundingBox : IPoint, fixEmbedding : bool) -> None:
		"""Implements the algorithm call."""
		...
