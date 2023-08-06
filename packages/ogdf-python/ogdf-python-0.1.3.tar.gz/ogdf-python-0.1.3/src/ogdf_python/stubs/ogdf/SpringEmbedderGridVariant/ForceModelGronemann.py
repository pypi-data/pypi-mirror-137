# file stubs/ogdf/SpringEmbedderGridVariant/ForceModelGronemann.py generated from classogdf_1_1_spring_embedder_grid_variant_1_1_force_model_gronemann
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
class ForceModelGronemann(ogdf.SpringEmbedderGridVariant.ForceModelBase):

	def __init__(self, vInfo : Array[NodeInfo], adjLists : Array[  int ], gridCell : Array2D[ListPure[  int ]], idealEdgeLength : float) -> None:
		...

	def computeDisplacement(self, j : int, boxLength : float) -> DPoint:
		...
