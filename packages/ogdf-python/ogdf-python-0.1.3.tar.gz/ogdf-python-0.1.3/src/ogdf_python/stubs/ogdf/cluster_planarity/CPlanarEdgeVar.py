# file stubs/ogdf/cluster_planarity/CPlanarEdgeVar.py generated from classogdf_1_1cluster__planarity_1_1_c_planar_edge_var
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
class CPlanarEdgeVar(ogdf.cluster_planarity.EdgeVar):

	@overload
	def __init__(self, master : abacus.Master, obj : float, lbound : float, source : node, target : node) -> None:
		...

	@overload
	def __init__(self, master : abacus.Master, obj : float, source : node, target : node) -> None:
		...

	def __destruct__(self) -> None:
		...

	def printMe(self, out : std.ostream) -> None:
		...
