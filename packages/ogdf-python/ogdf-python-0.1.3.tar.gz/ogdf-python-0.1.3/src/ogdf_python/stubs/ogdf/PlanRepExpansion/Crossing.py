# file stubs/ogdf/PlanRepExpansion/Crossing.py generated from structogdf_1_1_plan_rep_expansion_1_1_crossing
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
class Crossing(object):

	m_adj : adjEntry = ...

	m_partitionLeft : SList[adjEntry] = ...

	m_partitionRight : SList[adjEntry] = ...

	@overload
	def __init__(self) -> None:
		...

	@overload
	def __init__(self, adj : adjEntry) -> None:
		...
