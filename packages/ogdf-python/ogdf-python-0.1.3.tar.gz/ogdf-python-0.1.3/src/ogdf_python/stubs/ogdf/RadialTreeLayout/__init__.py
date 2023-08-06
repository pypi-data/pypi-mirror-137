# file stubs/ogdf/RadialTreeLayout/__init__.py generated from classogdf_1_1_radial_tree_layout
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
class RadialTreeLayout(ogdf.LayoutModule):

	"""The radial tree layout algorithm."""

	class RootSelectionType(enum.Enum):

		"""Selection strategies for root of the tree."""

		#: Select a source in the graph.
		Source = enum.auto()

		#: Select a sink in the graph.
		Sink = enum.auto()

		#: Select the center of the tree.
		Center = enum.auto()

	@overload
	def __init__(self) -> None:
		"""Creates an instance of radial tree layout and sets options to default values."""
		...

	@overload
	def __init__(self, tl : RadialTreeLayout) -> None:
		"""Copy constructor."""
		...

	def __destruct__(self) -> None:
		"""Destructor."""
		...

	def call(self, GA : GraphAttributes) -> None:
		"""Calls the algorithm for graph attributesGA."""
		...

	@overload
	def connectedComponentDistance(self) -> float:
		"""Returns the optionconnectedComponentDistance."""
		...

	@overload
	def connectedComponentDistance(self, x : float) -> None:
		"""Sets the optionconnectedComponentDistancetox."""
		...

	def diameter(self) -> NodeArray[ float ]:
		...

	def leaves(self) -> NodeArray[ float ]:
		...

	@overload
	def levelDistance(self) -> float:
		"""Returns the optionlevelDistance."""
		...

	@overload
	def levelDistance(self, x : float) -> None:
		"""Sets the optionlevelDistancetox."""
		...

	def __assign__(self, tl : RadialTreeLayout) -> RadialTreeLayout:
		"""Assignment operator."""
		...

	@overload
	def rootSelection(self) -> RootSelectionType:
		"""Returns the optionrootSelection."""
		...

	@overload
	def rootSelection(self, sel : RootSelectionType) -> None:
		"""Sets the optionrootSelectiontosel."""
		...
