# file stubs/ogdf/RankingModule.py generated from classogdf_1_1_ranking_module
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
class RankingModule(object):

	"""Interface of algorithms for computing a node ranking."""

	def __init__(self) -> None:
		"""Initializes a ranking module."""
		...

	def __destruct__(self) -> None:
		...

	@overload
	def call(self, G : Graph, _ : EdgeArray[  int ], _ : EdgeArray[  int ], rank : NodeArray[  int ]) -> None:
		...

	@overload
	def call(self, G : Graph, rank : NodeArray[  int ]) -> None:
		"""Computes a node ranking of the digraphGinrank."""
		...

	def __call__(self, G : Graph, rank : NodeArray[  int ]) -> None:
		"""Computes a node ranking of the digraphGinrank."""
		...
