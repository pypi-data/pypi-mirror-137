# file stubs/ogdf/LayoutModule.py generated from classogdf_1_1_layout_module
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
class LayoutModule(object):

	"""Interface of general layout algorithms."""

	def __init__(self) -> None:
		"""Initializes a layout module."""
		...

	def __destruct__(self) -> None:
		...

	def call(self, GA : GraphAttributes) -> None:
		"""Computes a layout of graphGA."""
		...

	def __call__(self, GA : GraphAttributes) -> None:
		"""Computes a layout of graphGA."""
		...
