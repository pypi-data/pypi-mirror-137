# file stubs/ogdf/SpringEmbedderGridVariant/ForceModelBase.py generated from classogdf_1_1_spring_embedder_grid_variant_1_1_force_model_base
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
class ForceModelBase(ogdf.spring_embedder.CommonForceModelBase[ NodeInfo ]):

	m_gridCell : Array2D[ListPure[  int ] ] = ...

	def __init__(self, vInfo : Array[NodeInfo], adjLists : Array[  int ], gridCell : Array2D[ListPure[  int ]], idealEdgeLength : float) -> None:
		...

	def __destruct__(self) -> None:
		...

	def computeDisplacement(self, j : int, boxLength : float) -> DPoint:
		...

	def computeMixedForcesDisplacement(self, j : int, boxLength : int, attractiveChange : Callable, attractiveFinal : Callable) -> DPoint:
		...

	def computeRepulsiveForce(self, j : int, boxLength : float, idealExponent : int, normExponent : int = 1) -> DPoint:
		...
