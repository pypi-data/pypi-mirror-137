# file stubs/ogdf/fast_multipole_embedder/GalaxyMultilevel/__init__.py generated from classogdf_1_1fast__multipole__embedder_1_1_galaxy_multilevel
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
class GalaxyMultilevel(object):

	NearSunList : Type = List[Tuple2[node,  int ] ]

	levelNumber : int = ...

	m_pCoarserMultiLevel : GalaxyMultilevel = ...

	m_pEdgeInfo : EdgeArray[LevelEdgeInfo] = ...

	m_pFinerMultiLevel : GalaxyMultilevel = ...

	m_pGraph : Graph = ...

	m_pNodeInfo : NodeArray[LevelNodeInfo] = ...

	@overload
	def __init__(self, prev : GalaxyMultilevel) -> None:
		...

	@overload
	def __init__(self, pGraph : Graph) -> None:
		...

	def __destruct__(self) -> None:
		...
