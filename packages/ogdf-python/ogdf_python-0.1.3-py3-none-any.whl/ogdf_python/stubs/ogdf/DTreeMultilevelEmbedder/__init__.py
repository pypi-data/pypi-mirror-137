# file stubs/ogdf/DTreeMultilevelEmbedder/__init__.py generated from classogdf_1_1_d_tree_multilevel_embedder
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
Dim = TypeVar('Dim')

class DTreeMultilevelEmbedder(Generic[Dim]):

	def __init__(self) -> None:
		"""constructor with a given graph, allocates memory and does initialization"""
		...

	def call(self, graph : Graph, coords : NodeArray[NodeCoords]) -> None:
		"""call the multilevel embedder layout for graph, the result is stored in coords"""
		...
