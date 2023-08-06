# file stubs/ogdf/UpwardPlanarity.py generated from classogdf_1_1_upward_planarity
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
class UpwardPlanarity(object):

	"""Upward planarity testing and embedding."""

	# General digraphs

	def isUpwardPlanar(self, G : Graph) -> bool:
		"""Tests whether graphGis upward planar (using satisfiability)."""
		...

	def embedUpwardPlanar(self, G : Graph, externalToItsRight : adjEntry) -> bool:
		"""Tests whether graphGis upward planar and embeds the graph by a upward planar embedding if possible (using satisfiability)."""
		...

	# Biconnected digraphs

	@overload
	def isUpwardPlanar_embedded(self, G : Graph) -> bool:
		"""Tests whether a biconnected graphGis upward planarly embedded."""
		...

	@overload
	def isUpwardPlanar_embedded(self, G : Graph, possibleExternalFaces : List[adjEntry]) -> bool:
		"""Tests whether a biconnected graphGis upward planarly embedded and computes the set of possible external faces."""
		...

	# Triconnected digraphs

	def isUpwardPlanar_triconnected(self, G : Graph) -> bool:
		"""Tests whether the triconnected digraphGis upward planar."""
		...

	def upwardPlanarEmbed_triconnected(self, G : Graph) -> bool:
		"""Upward planarly embeds the triconnected digraphG."""
		...

	# Single-source digraphs

	def isUpwardPlanar_singleSource(self, G : Graph) -> bool:
		"""Tests whether the single-source digraphGis upward planar."""
		...

	def upwardPlanarEmbed_singleSource(self, G : Graph) -> bool:
		"""Upward planarly embeds the single-source digraphG."""
		...

	@overload
	def upwardPlanarAugment_singleSource(self, G : Graph) -> bool:
		"""Tests whether single-source digraphGis upward planar, and if yes augments it to a planar st-digraph."""
		...

	@overload
	def upwardPlanarAugment_singleSource(self, G : Graph, superSink : node, augmentedEdges : SList[edge]) -> bool:
		"""Tests whether single-source digraphGis upward planar, and if yes augments it to a planar st-digraph."""
		...

	def isUpwardPlanar_singleSource_embedded(self, E : ConstCombinatorialEmbedding, externalFaces : SList[face]) -> bool:
		"""Tests whether the embeddingEof a single-source digraph is upward planar."""
		...

	def upwardPlanarAugment_singleSource_embedded(self, G : Graph, superSink : node, augmentedEdges : SList[edge]) -> bool:
		"""Tests if single-source digraphGis upward planarly embedded and augments it to a planar st-digraph."""
		...
