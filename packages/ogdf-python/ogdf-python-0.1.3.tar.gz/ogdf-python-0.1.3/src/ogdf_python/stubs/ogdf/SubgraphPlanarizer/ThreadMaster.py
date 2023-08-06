# file stubs/ogdf/SubgraphPlanarizer/ThreadMaster.py generated from classogdf_1_1_subgraph_planarizer_1_1_thread_master
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
class ThreadMaster(object):

	def __init__(self, pr : PlanRep, cc : int, pCost : EdgeArray[  int ], pForbid : EdgeArray[ bool ], pEdgeSubGraphs : EdgeArray[  int ], delEdges : List[edge], seed : int, perms : int, stopTime : int) -> None:
		...

	def __destruct__(self) -> None:
		...

	def cost(self) -> EdgeArray[  int ]:
		...

	def currentCC(self) -> int:
		...

	def delEdges(self) -> List[edge]:
		...

	def edgeSubGraphs(self) -> EdgeArray[  int ]:
		...

	def forbid(self) -> EdgeArray[ bool ]:
		...

	def getNextPerm(self) -> bool:
		...

	def planRep(self) -> PlanRep:
		...

	def postNewResult(self, pCS : CrossingStructure) -> CrossingStructure:
		...

	def queryBestKnown(self) -> int:
		...

	def restore(self, pr : PlanRep, cr : int) -> None:
		...

	def rseed(self, id : int) -> int:
		...
