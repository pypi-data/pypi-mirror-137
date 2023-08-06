# file stubs/ogdf/SugiyamaLayout.py generated from classogdf_1_1_sugiyama_layout
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
class SugiyamaLayout(ogdf.LayoutModule):

	"""Sugiyama's layout algorithm."""

	# Algorithm call

	@overload
	def call(self, GA : GraphAttributes) -> None:
		"""Calls the layout algorithm for graphGA."""
		...

	@overload
	def call(self, CGA : ClusterGraphAttributes) -> None:
		"""Calls the layout algorithm for clustered graphCGA."""
		...

	@overload
	def call(self, GA : GraphAttributes, rank : NodeArray[  int ]) -> None:
		"""Calls the layout algorithm for graphGAwith a given level assignment."""
		...

	def callUML(self, GA : GraphAttributes) -> None:
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
	def alignBaseClasses(self) -> bool:
		"""Returns the current setting of option alignBaseClasses."""
		...

	@overload
	def alignBaseClasses(self, b : bool) -> None:
		"""Sets the option alignBaseClasses tob."""
		...

	@overload
	def alignSiblings(self) -> bool:
		"""Returns the current setting of option alignSiblings."""
		...

	@overload
	def alignSiblings(self, b : bool) -> None:
		"""Sets the option alignSiblings tob."""
		...

	def setSubgraphs(self, esg : EdgeArray[  int ]) -> None:
		"""Sets the subgraphs for simultaneous drawing."""
		...

	def useSubgraphs(self) -> bool:
		"""Returns true iff subgraphs for simultaneous drawing are set."""
		...

	@overload
	def permuteFirst(self) -> bool:
		...

	@overload
	def permuteFirst(self, b : bool) -> None:
		...

	@overload
	def maxThreads(self) -> int:
		"""Returns the maximal number of used threads."""
		...

	@overload
	def maxThreads(self, n : int) -> None:
		"""Sets the maximal number of used threads ton."""
		...

	# Module options

	def setRanking(self, pRanking : RankingModule) -> None:
		"""Sets the module option for the node ranking (layer assignment)."""
		...

	def setCrossMin(self, pCrossMin : LayeredCrossMinModule) -> None:
		"""Sets the module option for the two-layer crossing minimization."""
		...

	def setLayout(self, pLayout : HierarchyLayoutModule) -> None:
		"""Sets the module option for the computation of the final layout."""
		...

	def setClusterLayout(self, pLayout : HierarchyClusterLayoutModule) -> None:
		"""Sets the module option for the computation of the final layout for clustered graphs."""
		...

	def setPacker(self, pPacker : CCLayoutPackModule) -> None:
		"""Sets the module option for the arrangement of connected components."""
		...

	# Information after call

	def numberOfCrossings(self) -> int:
		"""Returns the number of crossings in the computed layout (usual graph)."""
		...

	def numberOfCrossingsCluster(self) -> RCCrossings:
		"""Returns the number of crossings in the computed layout (cluster graph)."""
		...

	def numberOfLevels(self) -> int:
		"""Return the number of layers/levels}."""
		...

	def maxLevelSize(self) -> int:
		"""Return the max. number of elements on a layer."""
		...

	def timeReduceCrossings(self) -> float:
		...

	def subgraphs(self) -> EdgeArray[  int ]:
		...

	def numCC(self) -> int:
		...

	def compGC(self) -> NodeArray[  int ]:
		...

	@overload
	def reduceCrossings(self, H : ExtendedNestingGraph) -> None:
		...

	@overload
	def reduceCrossings(self, H : Hierarchy) -> HierarchyLevelsBase:
		...

	#: Option for aligning base classes.
	m_alignBaseClasses : bool = ...

	#: Option for aligning siblings in inheritance trees.
	m_alignSiblings : bool = ...

	#: Option for laying out components separately.
	m_arrangeCCs : bool = ...

	#: the hierarchy cluster layout module (final coordinate assignment for clustered graphs)
	m_clusterLayout : std.unique_ptr[HierarchyClusterLayoutModule] = ...

	#: the module for two-layer crossing minimization
	m_crossMin : std.unique_ptr[LayeredCrossMinModule] = ...

	m_crossMinSimDraw : std.unique_ptr[TwoLayerCrossMinSimDraw] = ...

	#: Option for maximal number of fails.
	m_fails : int = ...

	#: the hierarchy layout module (final coordinate assignment)
	m_layout : std.unique_ptr[HierarchyLayoutModule] = ...

	m_levelChanged : Array[ bool ] = ...

	#: The maximal number of used threads.
	m_maxThreads : int = ...

	#: Option for distance between connected components.
	m_minDistCC : float = ...

	#: Number of crossings in computed layout.
	m_nCrossings : int = ...

	m_nCrossingsCluster : RCCrossings = ...

	#: The module for arranging connected components.
	m_packer : std.unique_ptr[CCLayoutPackModule] = ...

	#: Option for desired page ratio.
	m_pageRatio : float = ...

	m_permuteFirst : bool = ...

	#: the ranking module (level assignment)
	m_ranking : std.unique_ptr[RankingModule] = ...

	#: Option for number of runs.
	m_runs : int = ...

	#: Defines the subgraphs for simultaneous drawing.
	m_subgraphs : EdgeArray[  int ] = ...

	#: Option for switching on transposal heuristic.
	m_transpose : bool = ...

	def __init__(self) -> None:
		"""Creates an instance ofSugiyamaLayoutand sets options to default values."""
		...

	def __destruct__(self) -> None:
		...
