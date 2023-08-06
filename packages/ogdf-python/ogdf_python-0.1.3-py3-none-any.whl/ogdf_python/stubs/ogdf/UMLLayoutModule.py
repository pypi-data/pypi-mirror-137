# file stubs/ogdf/UMLLayoutModule.py generated from classogdf_1_1_u_m_l_layout_module
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
class UMLLayoutModule(object):

	"""Interface of UML layout algorithms."""

	def __init__(self) -> None:
		"""Initializes a UML layout module."""
		...

	def __destruct__(self) -> None:
		...

	def call(self, umlGraph : UMLGraph) -> None:
		"""Computes a layout of UML graphumlGraph."""
		...

	def __call__(self, umlGraph : UMLGraph) -> None:
		"""Computes a layout of UML graphumlGraph."""
		...
