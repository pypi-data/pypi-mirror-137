# file stubs/ogdf/topology_module/EdgeLeg.py generated from classogdf_1_1topology__module_1_1_edge_leg
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
class EdgeLeg(object):

	"""Helper class for the computation of crossings."""

	#: each edgeLeg holds an entry with a ListIterator pointing to its entry in a <edgeLeg*>Listfor an original edge
	m_eIterator : ListIterator[EdgeLeg] = ...

	#: we store the direction of the crossedEdgeLeg, too if crossingEdgeLeg is horizontally left to right
	m_topDown : bool = ...

	#: to avoid sorting both edgelegs and crossing points, do not store a pair of them, but allow the xp to be stored in the edgeleg
	m_xp : DPoint = ...

	@overload
	def __init__(self) -> None:
		...

	@overload
	def __init__(self, e : edge, number : int, p1 : DPoint, p2 : DPoint) -> None:
		...

	def copyEdge(self) -> edge:
		...

	def end(self) -> DPoint:
		...

	def number(self) -> int:
		...

	def start(self) -> DPoint:
		...
