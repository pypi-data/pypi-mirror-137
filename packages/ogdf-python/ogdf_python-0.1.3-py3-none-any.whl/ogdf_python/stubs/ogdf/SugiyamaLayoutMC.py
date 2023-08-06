# file stubs/ogdf/SugiyamaLayoutMC.py generated from classogdf_1_1_sugiyama_layout_m_c
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
class SugiyamaLayoutMC(ogdf.LayoutModule):

	"""Sugiyama's layout algorithm."""

	# Algorithm call

	@overload
	def call(self, GA : GraphAttributes) -> None:
		"""Calls the layout algorithm for graphGA."""
		...

	@overload
	def call(self, GA : GraphAttributes, rank : NodeArray[  int ]) -> None:
		"""Calls the layout algorithm for graphGAwith a given level assignment."""
		...

	# Optional parameters

	@overload
	def fails(self) -> int:
		"""Returns the current setting of option fails."""
		...

	@overload
	def fails(self, nFails : int) -> None:
		"""Sets the option fails tonFails."""
		...

	@overload
	def runs(self) -> int:
		"""Returns the current setting of option runs."""
		...

	@overload
	def runs(self, nRuns : int) -> None:
		"""Sets the option runs tonRuns."""
		...

	@overload
	def transpose(self) -> bool:
		"""Returns the current setting of option transpose."""
		...

	@overload
	def transpose(self, bTranspose : bool) -> None:
		"""Sets the option transpose tobTranspose."""
		...

	@overload
	def arrangeCCs(self) -> bool:
		"""Returns the current setting of option arrangeCCs."""
		...

	@overload
	def arrangeCCs(self, bArrange : bool) -> None:
		"""Sets the options arrangeCCs tobArrange."""
		...

	@overload
	def minDistCC(self) -> float:
		"""Returns the current setting of option minDistCC (distance between components)."""
		...

	@overload
	def minDistCC(self, x : float) -> None:
		"""Sets the option minDistCC tox."""
		...

	@overload
	def pageRatio(self) -> float:
		"""Returns the current setting of option pageRation."""
		...

	@overload
	def pageRatio(self, x : float) -> None:
		"""Sets the option pageRatio tox."""
		...

	@overload
	def permuteFirst(self) -> bool:
		...

	@overload
	def permuteFirst(self, b : bool) -> None:
		...

	@overload
	def evenOdd(self) -> bool:
		...

	@overload
	def evenOdd(self, b : bool) -> None:
		...

	@overload
	def sortAfterLayers(self) -> int:
		...

	@overload
	def sortAfterLayers(self, n : int) -> None:
		...

	# Module options

	def setRanking(self, pRanking : RankingModule) -> None:
		"""Sets the module option for the node ranking (layer assignment)."""
		...

	def setLayout(self, pLayout : HierarchyLayoutModule) -> None:
		"""Sets the module option for the computation of the final layout."""
		...

	def setPacker(self, pPacker : CCLayoutPackModule) -> None:
		"""Sets the module option for the arrangement of connected components."""
		...

	# Information after call

	def numberOfCrossings(self) -> int:
		"""Returns the number of crossings in the computed layout (usual graph)."""
		...

	def numberOfLevels(self) -> int:
		"""Return the number of layers/levels."""
		...

	def maxLevelSize(self) -> int:
		"""Return the max. number of elements on a layer."""
		...

	def timeReduceCrossings(self) -> float:
		...

	def reduceCrossings(self, levels : HierarchyLevels) -> None:
		...

	def reduceCrossingsEvenOdd(self, levels : HierarchyLevels) -> None:
		...

	def barycenter(self, level : Level, doSorting : bool) -> None:
		...

	#: Option for laying out components separately.
	m_arrangeCCs : bool = ...

	m_evenOdd : bool = ...

	#: Option for maximal number of fails.
	m_fails : int = ...

	#: the hierarchy layout module (final coordinate assignment)
	m_layout : std.unique_ptr[HierarchyLayoutModule] = ...

	m_levelChanged : Array[ bool ] = ...

	#: Option for distance between connected components.
	m_minDistCC : float = ...

	#: Number of crossings in computed layout.
	m_nCrossings : int = ...

	#: The module for arranging connected components.
	m_packer : std.unique_ptr[CCLayoutPackModule] = ...

	#: Option for desired page ratio.
	m_pageRatio : float = ...

	m_permuteFirst : bool = ...

	#: the ranking module (level assignment)
	m_ranking : std.unique_ptr[RankingModule] = ...

	#: Option for number of runs.
	m_runs : int = ...

	m_sortAfterLayers : int = ...

	#: Option for switching on transposal heuristic.
	m_transpose : bool = ...

	def __init__(self) -> None:
		"""Creates an instance ofSugiyamaLayoutand sets options to default values."""
		...

	def __destruct__(self) -> None:
		...
