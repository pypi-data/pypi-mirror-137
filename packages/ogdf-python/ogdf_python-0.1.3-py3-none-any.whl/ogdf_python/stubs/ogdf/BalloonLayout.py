# file stubs/ogdf/BalloonLayout.py generated from classogdf_1_1_balloon_layout
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
class BalloonLayout(ogdf.LayoutModule):

	class ChildOrder(enum.Enum):

		Fixed = enum.auto()

		Optimized = enum.auto()

	class RootSelection(enum.Enum):

		Center = enum.auto()

		HighestDegree = enum.auto()

	class TreeComputation(enum.Enum):

		Bfs = enum.auto()

		Dfs = enum.auto()

		BfsRandom = enum.auto()

	def __init__(self) -> None:
		"""Constructor, sets options to default values."""
		...

	def call(self, AG : GraphAttributes) -> None:
		"""Standard call using the stored parameter settings."""
		...

	def callFractal(self, AG : GraphAttributes, ratio : float = 0.3) -> None:
		"""Call using special parameter settings for fractal model takes radius ratio < 0.5 as parameter."""
		...

	def getEvenAngles(self) -> bool:
		"""returns how the angles are assigned to subtrees."""
		...

	def __assign__(self, bl : BalloonLayout) -> BalloonLayout:
		"""Assignmentoperator."""
		...

	def setEvenAngles(self, b : bool) -> None:
		"""Subtrees may be assigned even angles or angles depending on their size."""
		...

	def computeAngles(self, G : Graph) -> None:
		"""Computes the angle distribution: assigns m_angle each node."""
		...

	def computeBFSTree(self, G : Graph, v : node) -> None:
		"""Computes tree by BFS, fills m_parent and m_childCount."""
		...

	def computeCoordinates(self, AG : GraphAttributes) -> None:
		"""Computes coordinates from angles and radii."""
		...

	def computeRadii(self, AG : GraphAttributes) -> None:
		"""Computes a radius for each of the vertices in G. fractal model: same radius on same level, such that r(m) = gamma* r(m-1) where gamma is predefined SNS model: different radii possible Optimal: unordered tree, order of children is optimized."""
		...

	def computeTree(self, G : Graph) -> None:
		"""Computes the spanning tree that is used for the layout computation, the non-tree edges are simply added into the layout."""
		...

	def selectRoot(self, G : Graph) -> None:
		"""Selects the root of the spanning tree that is placed in the layout center."""
		...
