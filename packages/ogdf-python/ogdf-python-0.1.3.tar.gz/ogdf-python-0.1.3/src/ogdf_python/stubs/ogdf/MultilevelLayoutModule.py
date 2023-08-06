# file stubs/ogdf/MultilevelLayoutModule.py generated from classogdf_1_1_multilevel_layout_module
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
class MultilevelLayoutModule(ogdf.LayoutModule):

	"""Interface of general layout algorithms that also allow aMultilevelGraphas call parameter, extending the interface of a simpleLayoutModule."""

	def __init__(self) -> None:
		"""Initializes a multilevel layout module."""
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
