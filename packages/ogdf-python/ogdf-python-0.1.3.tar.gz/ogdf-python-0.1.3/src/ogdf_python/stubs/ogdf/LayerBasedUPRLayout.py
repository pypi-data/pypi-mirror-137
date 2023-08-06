# file stubs/ogdf/LayerBasedUPRLayout.py generated from classogdf_1_1_layer_based_u_p_r_layout
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
class LayerBasedUPRLayout(ogdf.UPRLayoutModule):

	# UPRLayoutSimple methods

	m_crossings : int = ...

	m_layout : std.unique_ptr[HierarchyLayoutModule] = ...

	m_ranking : std.unique_ptr[RankingModule] = ...

	def __init__(self) -> None:
		...

	def __destruct__(self) -> None:
		...

	def maxLayerSize(self) -> int:
		"""Return the max. number of elements on a layer. Not implemented if use methode callSimple(..)."""
		...

	def numberOfCrossings(self) -> int:
		...

	def numberOfLayers(self) -> int:
		"""Return the number of layers/levels. Not implemented if use methode callSimple(..)."""
		...

	def setLayout(self, pLayout : HierarchyLayoutModule) -> None:
		...

	def setRanking(self, pRanking : RankingModule) -> None:
		...

	def UPRLayoutSimple(self, UPR : UpwardPlanRep, AG : GraphAttributes) -> None:
		"""Use only the 3. phase of Sugiyama' framework for layout."""
		...

	def doCall(self, UPR : UpwardPlanRep, AG : GraphAttributes) -> None:
		"""Implements the actual algorithm call."""
		...
