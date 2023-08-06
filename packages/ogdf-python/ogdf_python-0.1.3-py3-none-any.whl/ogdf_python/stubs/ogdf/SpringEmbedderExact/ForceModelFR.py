# file stubs/ogdf/SpringEmbedderExact/ForceModelFR.py generated from classogdf_1_1_spring_embedder_exact_1_1_force_model_f_r
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
class ForceModelFR(ogdf.SpringEmbedderExact.ForceModelBase):

	def __init__(self, vInfo : Array[NodeInfo], adjLists : Array[  int ], idealEdgeLength : float) -> None:
		...

	def computeDisplacement(self, j : int) -> DPoint:
		...
