# file stubs/ogdf/LayoutStandards.py generated from classogdf_1_1_layout_standards
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
class LayoutStandards(object):

	"""Standard values for graphical attributes and layouts."""

	# Global default node attributes

	def defaultNodeWidth(self) -> float:
		"""Returns the global default width for nodes."""
		...

	def setDefaultNodeWidth(self, w : float) -> None:
		"""Sets the global default width for nodes tow."""
		...

	def defaultNodeHeight(self) -> float:
		"""Returns the global default height for nodes."""
		...

	def setDefaultNodeHeight(self, h : float) -> None:
		"""Sets the global default height for nodes toh."""
		...

	def defaultNodeShape(self) -> Shape:
		"""Returns the global default shape for nodes."""
		...

	def setDefaultNodeShape(self, s : Shape) -> None:
		"""Sets the global default shape for nodes tos."""
		...

	def defaultNodeStroke(self) -> Stroke:
		"""Returns the global default stroke for nodes."""
		...

	def defaultNodeStrokeColor(self) -> Color:
		"""Returns the global default stroke color for nodes."""
		...

	def defaultNodeStrokeWidth(self) -> float:
		"""Returns the global default stroke width for nodes."""
		...

	def setDefaultNodeStroke(self, stroke : Stroke) -> None:
		"""Sets the global default stroke for nodes tostroke."""
		...

	def defaultNodeFill(self) -> Fill:
		"""Returns the global default fill for nodes."""
		...

	def defaultNodeFillColor(self) -> Color:
		"""Returns the global default fill color for nodes."""
		...

	def setDefaultNodeFill(self, fill : Fill) -> None:
		"""Sets the global default fill for nodes tofill."""
		...

	# Global default edge attributes

	def defaultEdgeStroke(self) -> Stroke:
		"""Returns the global default stroke for edges."""
		...

	def defaultEdgeStrokeColor(self) -> Color:
		"""Returns the global default stroke color for edges."""
		...

	def defaultEdgeStrokeWidth(self) -> float:
		"""Returns the global default stroke width for edges."""
		...

	def setDefaultEdgeStroke(self, stroke : Stroke) -> None:
		"""Sets the global default stroke for edges tostroke."""
		...

	def defaultEdgeArrow(self) -> EdgeArrow:
		"""Returns the global default arrow type for edges."""
		...

	def setDefaultEdgeArrow(self, arrow : EdgeArrow) -> None:
		"""Sets the global default arrow type for edges toarrow."""
		...

	# Global default cluster attributes

	def defaultClusterStroke(self) -> Stroke:
		"""Returns the global default stroke for clusters."""
		...

	def defaultClusterStrokeColor(self) -> Color:
		"""Returns the global default stroke color for clusters."""
		...

	def defaultClusterStrokeWidth(self) -> float:
		"""Returns the global default stroke width for clusters."""
		...

	def setDefaultClusterStroke(self, stroke : Stroke) -> None:
		"""Sets the global default stroke for cluster tostroke."""
		...

	def defaultClusterFill(self) -> Fill:
		"""Returns the global default fill for clusters."""
		...

	def defaultClusterFillColor(self) -> Color:
		"""Returns the global default fill color for clusters."""
		...

	def setDefaultClusterFill(self, fill : Fill) -> None:
		"""Sets the global default fill for clusters tofill."""
		...

	# Global default separation parameters

	def defaultNodeSeparation(self) -> float:
		"""Returns the global default node separation."""
		...

	def setDefaultNodeSeparation(self, d : float) -> None:
		"""Sets the global default node separation tod."""
		...

	def defaultCCSeparation(self) -> float:
		"""Returns the global default separation between connected components."""
		...

	def setDefaultCCSeparation(self, d : float) -> None:
		"""Sets the global default separation between connected components tod."""
		...
