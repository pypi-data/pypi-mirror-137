# file stubs/ogdf/UpwardPlanaritySingleSource/SkeletonInfo.py generated from classogdf_1_1_upward_planarity_single_source_1_1_skeleton_info
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
class SkeletonInfo(object):

	m_containsSource : EdgeArray[ bool ] = ...

	m_degInfo : EdgeArray[DegreeInfo] = ...

	m_E : ConstCombinatorialEmbedding = ...

	m_externalFaces : SList[face] = ...

	m_F : FaceSinkGraph = ...

	@overload
	def __init__(self) -> None:
		...

	@overload
	def __init__(self, S : Skeleton) -> None:
		...

	def init(self, S : Skeleton) -> None:
		...
