# file stubs/ogdf/fast_multipole_embedder/FMEBasicKernel.py generated from classogdf_1_1fast__multipole__embedder_1_1_f_m_e_basic_kernel
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
class FMEBasicKernel(object):

	def edgeForces(self, graph : ArrayGraph, fx : float, fy : float) -> None:
		...

	def moveNodes(self, graph : ArrayGraph, fx : float, fy : float, timeStep : float) -> float:
		...

	def repForces(self, graph : ArrayGraph, fx : float, fy : float) -> None:
		...

	def simpleEdgeIteration(self, graph : ArrayGraph, fx : float, fy : float, timeStep : float) -> float:
		...

	def simpleForceDirected(self, graph : ArrayGraph, timeStep : float, minIt : int, maxIt : int, preProcIt : int, threshold : float) -> None:
		...

	def simpleIteration(self, graph : ArrayGraph, fx : float, fy : float, timeStep : float) -> float:
		...
