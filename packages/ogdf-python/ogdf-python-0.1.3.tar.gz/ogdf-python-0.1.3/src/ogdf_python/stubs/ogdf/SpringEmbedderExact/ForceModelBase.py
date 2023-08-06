# file stubs/ogdf/SpringEmbedderExact/ForceModelBase.py generated from classogdf_1_1_spring_embedder_exact_1_1_force_model_base
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
class ForceModelBase(ogdf.spring_embedder.CommonForceModelBase[ NodeInfo ]):

	m_ca : float = ...

	m_cr : float = ...

	def __init__(self, vInfo : Array[NodeInfo], adjLists : Array[  int ], idealEdgeLength : float) -> None:
		...

	def __destruct__(self) -> None:
		...

	def computeDisplacement(self, j : int) -> DPoint:
		...

	def computeMixedForces(self, forceAttr : DPoint, forceRep : DPoint, j : int, attractiveChange : Callable) -> None:
		...

	def computeRepulsiveForce(self, j : int, idealExponent : int, normExponent : int = 1) -> DPoint:
		...
