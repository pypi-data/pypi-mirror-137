# file stubs/ogdf/ForceLayoutModule.py generated from classogdf_1_1_force_layout_module
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
class ForceLayoutModule(ogdf.LayoutModule):

	"""Interface of general layout algorithms."""

	def __init__(self) -> None:
		"""Initializes a force layout module."""
		...

	def __destruct__(self) -> None:
		...

	@overload
	def call(self, GA : GraphAttributes) -> None:
		"""Computes a layout of graphGA."""
		...

	@overload
	def call(self, MLG : MultilevelGraph) -> None:
		"""Computes a layout of graphMLG."""
		...
