# file stubs/ogdf/ClusterPlanarModule.py generated from classogdf_1_1_cluster_planar_module
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
class ClusterPlanarModule(ogdf.Module):

	def __init__(self) -> None:
		...

	def __destruct__(self) -> None:
		...

	def isClusterPlanar(self, CG : ClusterGraph) -> bool:
		"""Returns true, if CG is c-planar, false otherwise."""
		...

	def doTest(self, CG : ClusterGraph) -> bool:
		"""Performs a c-planarity test on CG."""
		...
