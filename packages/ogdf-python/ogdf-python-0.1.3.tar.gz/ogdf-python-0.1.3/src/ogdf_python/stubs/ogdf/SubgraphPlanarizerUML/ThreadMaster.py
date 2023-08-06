# file stubs/ogdf/SubgraphPlanarizerUML/ThreadMaster.py generated from classogdf_1_1_subgraph_planarizer_u_m_l_1_1_thread_master
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
class ThreadMaster(object):

	def __init__(self, pr : PlanRep, cc : int, pCost : EdgeArray[  int ], delEdges : List[edge], seed : int, perms : int, stopTime : int) -> None:
		...

	def __destruct__(self) -> None:
		...

	def cost(self) -> EdgeArray[  int ]:
		...

	def currentCC(self) -> int:
		...

	def delEdges(self) -> List[edge]:
		...

	def getNextPerm(self) -> bool:
		...

	def planRep(self) -> PlanRep:
		...

	def postNewResult(self, pCS : CrossingStructure) -> CrossingStructure:
		...

	def queryBestKnown(self) -> int:
		...

	def restore(self, PG : PlanRep, cr : int) -> None:
		...

	def rseed(self, id : int) -> int:
		...
