# file stubs/ogdf/spring_embedder/CommonForceModelBase.py generated from classogdf_1_1spring__embedder_1_1_common_force_model_base
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
NodeInfo = TypeVar('NodeInfo')

class CommonForceModelBase(Generic[NodeInfo]):

	m_adjLists : Array[  int ] = ...

	m_idealEdgeLength : float = ...

	m_vInfo : Array[ NodeInfo ] = ...

	def __init__(self, vInfo : Array[ NodeInfo ], adjLists : Array[  int ], idealEdgeLength : float) -> None:
		...

	def eps(self) -> float:
		...

	def computeFruchtermanReingoldAttractiveForce(self, j : int, idealExponent : int) -> DPoint:
		...

	def normByIdealEdgeLength(self, norm : float) -> float:
		...
