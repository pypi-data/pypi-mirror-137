# file stubs/ogdf/SpringEmbedderExact/Master.py generated from classogdf_1_1_spring_embedder_exact_1_1_master
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
class Master(ogdf.spring_embedder.MasterBase[ NodeInfo, ForceModelBase ]):

	def __init__(self, spring : SpringEmbedderExact, gc : GraphCopy, ga : GraphAttributes, boundingBox : DPoint) -> None:
		...

	def collectForces(self, sumForces : float, maxForce : float) -> None:
		...

	def computeFinalBB(self) -> None:
		...

	def initialize(self, wsum : float, hsum : float, xmin : float, xmax : float, ymin : float, ymax : float) -> None:
		...

	def scaleLayout(self, sumLengths : float) -> None:
		...

	def xmin(self) -> float:
		...

	def ymin(self) -> float:
		...
