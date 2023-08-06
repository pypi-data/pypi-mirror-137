# file stubs/ogdf/PlanRep/Deg1RestoreInfo.py generated from structogdf_1_1_plan_rep_1_1_deg1_restore_info
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
class Deg1RestoreInfo(object):

	"""Information for restoring degree-1 nodes."""

	#: the reference adjacency entry for restoring the edge
	m_adjRef : adjEntry = ...

	#: the original deg-1 node
	m_deg1Original : node = ...

	#: the original edge leading to the deg-1 node
	m_eOriginal : edge = ...

	@overload
	def __init__(self) -> None:
		...

	@overload
	def __init__(self, eOrig : edge, deg1Orig : node, adjRef : adjEntry) -> None:
		...
