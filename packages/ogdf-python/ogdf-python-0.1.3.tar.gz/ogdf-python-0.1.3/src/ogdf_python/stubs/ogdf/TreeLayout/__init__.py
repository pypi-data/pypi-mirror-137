# file stubs/ogdf/TreeLayout/__init__.py generated from classogdf_1_1_tree_layout
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
class TreeLayout(ogdf.LayoutModule):

	"""The tree layout algorithm."""

	# Algorithm call

	def call(self, GA : GraphAttributes) -> None:
		"""Calls tree layout for graph attributesGA."""
		...

	def callSortByPositions(self, GA : GraphAttributes, G : Graph) -> None:
		"""Calls tree layout for graph attributesGA."""
		...

	# Optional parameters

	@overload
	def siblingDistance(self) -> float:
		"""Returns the the minimal required horizontal distance between siblings."""
		...

	@overload
	def siblingDistance(self, x : float) -> None:
		"""Sets the the minimal required horizontal distance between siblings tox."""
		...

	@overload
	def subtreeDistance(self) -> float:
		"""Returns the minimal required horizontal distance between subtrees."""
		...

	@overload
	def subtreeDistance(self, x : float) -> None:
		"""Sets the minimal required horizontal distance between subtrees tox."""
		...

	@overload
	def levelDistance(self) -> float:
		"""Returns the minimal required vertical distance between levels."""
		...

	@overload
	def levelDistance(self, x : float) -> None:
		"""Sets the minimal required vertical distance between levels tox."""
		...

	@overload
	def treeDistance(self) -> float:
		"""Returns the minimal required horizontal distance between trees in the forest."""
		...

	@overload
	def treeDistance(self, x : float) -> None:
		"""Sets the minimal required horizontal distance between trees in the forest tox."""
		...

	@overload
	def orthogonalLayout(self) -> bool:
		"""Returns whether orthogonal edge routing style is used."""
		...

	@overload
	def orthogonalLayout(self, b : bool) -> None:
		"""Sets the option for orthogonal edge routing style tob."""
		...

	@overload
	def orientation(self) -> Orientation:
		"""Returns the option that determines the orientation of the layout."""
		...

	@overload
	def orientation(self, orientation : Orientation) -> None:
		"""Sets the option that determines the orientation of the layout toorientation."""
		...

	@overload
	def rootSelection(self) -> RootSelectionType:
		"""Returns the option that determines how the root is selected."""
		...

	@overload
	def rootSelection(self, rootSelection : RootSelectionType) -> None:
		"""Sets the option that determines how the root is selected torootSelection."""
		...

	# Operators

	def __assign__(self, tl : TreeLayout) -> TreeLayout:
		"""Assignment operator."""
		...

	class RootSelectionType(enum.Enum):

		"""Determines how to select the root of the tree."""

		#: Select a source in the graph.
		Source = enum.auto()

		#: Select a sink in the graph.
		Sink = enum.auto()

		#: Use the coordinates, e.g., select the topmost node if orientation is topToBottom.
		ByCoord = enum.auto()

	@overload
	def __init__(self) -> None:
		"""Creates an instance of tree layout and sets options to default values."""
		...

	@overload
	def __init__(self, tl : TreeLayout) -> None:
		"""Copy constructor."""
		...

	def __destruct__(self) -> None:
		"""Destructor."""
		...
