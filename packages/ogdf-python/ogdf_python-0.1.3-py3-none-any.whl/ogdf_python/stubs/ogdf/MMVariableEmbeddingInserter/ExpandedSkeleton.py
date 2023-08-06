# file stubs/ogdf/MMVariableEmbeddingInserter/ExpandedSkeleton.py generated from classogdf_1_1_m_m_variable_embedding_inserter_1_1_expanded_skeleton
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
class ExpandedSkeleton(object):

	def __init__(self, BC : Block) -> None:
		...

	def constructDual(self, bPathToEdge : bool, bPathToSrc : bool, bPathToTgt : bool) -> None:
		...

	def expand(self, v : node, eIn : edge, eOut : edge) -> None:
		...

	def findShortestPath(self, bPathToEdge : bool, bPathToSrc : bool, bPathToTgt : bool, paths : Paths) -> None:
		...

	def __assign__(self, _ : ExpandedSkeleton) -> ExpandedSkeleton:
		...
