# file stubs/ogdf/HananiTutteCPlanarity/CGraph.py generated from classogdf_1_1_hanani_tutte_c_planarity_1_1_c_graph
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
class CGraph(object):

	def __init__(self, C : ClusterGraph) -> None:
		...

	def cpcheck(self, nRows : int, nCols : int) -> Verification:
		...

	def cplanar(self, nRows : int, nCols : int) -> bool:
		...

	def timeCreateSparse(self) -> int:
		...

	def timePrepare(self) -> int:
		...

	def timesolve(self) -> int:
		...
