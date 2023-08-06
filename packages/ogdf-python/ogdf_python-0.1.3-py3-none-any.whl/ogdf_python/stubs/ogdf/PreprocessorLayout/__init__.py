# file stubs/ogdf/PreprocessorLayout/__init__.py generated from classogdf_1_1_preprocessor_layout
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
class PreprocessorLayout(ogdf.MultilevelLayoutModule):

	"""ThePreprocessorLayoutremoves multi-edges and self-loops."""

	def __init__(self) -> None:
		"""Constructor."""
		...

	def __destruct__(self) -> None:
		"""Destructor."""
		...

	@overload
	def call(self, GA : GraphAttributes) -> None:
		"""Calculates a drawing for theGraphGA."""
		...

	@overload
	def call(self, GA : GraphAttributes) -> None:
		"""Computes a layout of graphGA."""
		...

	@overload
	def call(self, MLG : MultilevelGraph) -> None:
		"""Computes a layout of graphMLG."""
		...

	@overload
	def call(self, MLG : MultilevelGraph) -> None:
		"""Calculates a drawing for theGraphMLG."""
		...

	def setLayoutModule(self, layout : LayoutModule) -> None:
		"""Sets the secondary layout."""
		...

	def setRandomizePositions(self, on : bool) -> None:
		"""Defines whether the positions of the node are randomized before the secondary layout call."""
		...
