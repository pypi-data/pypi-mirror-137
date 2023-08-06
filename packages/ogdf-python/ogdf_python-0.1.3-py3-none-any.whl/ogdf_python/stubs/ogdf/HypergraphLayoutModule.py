# file stubs/ogdf/HypergraphLayoutModule.py generated from classogdf_1_1_hypergraph_layout_module
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
class HypergraphLayoutModule(object):

	"""Interface of hypergraph layout algorithms."""

	OGDF_MALLOC_NEW_DELETE = ...

	def __init__(self) -> None:
		"""Initializes a layout module."""
		...

	def __destruct__(self) -> None:
		...

	def call(self, HA : HypergraphAttributes) -> None:
		"""Computes a layout of hypergraph given byHA."""
		...

	def __call__(self, HA : HypergraphAttributes) -> None:
		"""Computes a layout of a hypergraph given byHA."""
		...
