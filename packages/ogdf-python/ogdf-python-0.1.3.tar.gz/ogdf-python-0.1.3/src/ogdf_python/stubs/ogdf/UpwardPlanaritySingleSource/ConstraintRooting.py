# file stubs/ogdf/UpwardPlanaritySingleSource/ConstraintRooting.py generated from classogdf_1_1_upward_planarity_single_source_1_1_constraint_rooting
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
class ConstraintRooting(object):

	def __init__(self, T : SPQRTree) -> None:
		...

	def constrainRealEdge(self, e : edge) -> None:
		...

	def constrainTreeEdge(self, e : edge, src : node) -> bool:
		...

	def findRooting(self) -> edge:
		...

	def __assign__(self, _ : ConstraintRooting) -> ConstraintRooting:
		...

	def outputConstraints(self, os : std.ostream) -> None:
		...
