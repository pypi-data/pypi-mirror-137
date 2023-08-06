# file stubs/ogdf/fast_multipole_embedder/FMESingleKernel.py generated from classogdf_1_1fast__multipole__embedder_1_1_f_m_e_single_kernel
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
class FMESingleKernel(ogdf.fast_multipole_embedder.FMEBasicKernel):

	def __call__(self, graph : ArrayGraph, timeStep : float, minIt : int, maxIt : int, threshold : float) -> None:
		...
