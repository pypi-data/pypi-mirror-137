# file stubs/ogdf/UpwardPlanaritySingleSource/__init__.py generated from classogdf_1_1_upward_planarity_single_source
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
class UpwardPlanaritySingleSource(object):

	"""Performs upward planarity testing and embedding for single-source digraphs."""

	# Computation of st-skeletons

	# Embedding of skeletons

	# Assigning sinks to faces

	# For testing / debugging only

	def embedAndAugment(self, G : Graph, adjacentEdges : NodeArray[SListPure[adjEntry] ], augment : bool, superSink : node, augmentedEdges : SList[edge]) -> None:
		...

	def testAndFindEmbedding(self, G : Graph, embed : bool, adjacentEdges : NodeArray[SListPure[adjEntry] ]) -> bool:
		...
