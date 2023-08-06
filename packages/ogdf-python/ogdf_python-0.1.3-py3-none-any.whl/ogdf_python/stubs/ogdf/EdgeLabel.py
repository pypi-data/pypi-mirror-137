# file stubs/ogdf/EdgeLabel.py generated from classogdf_1_1_edge_label
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
coordType = TypeVar('coordType')

class EdgeLabel(Generic[coordType]):

	numberUsedLabels : int = ...

	@overload
	def __init__(self) -> None:
		...

	@overload
	def __init__(self, rhs : EdgeLabel) -> None:
		...

	@overload
	def __init__(self, e : edge, w : coordType, h : coordType, usedLabels : int) -> None:
		...

	@overload
	def __init__(self, e : edge, w : coordType, h : coordType, usedLabels : int = numberUsedLabels) -> None:
		...

	@overload
	def __init__(self, e : edge, usedLabels : int = numberUsedLabels) -> None:
		...

	def __destruct__(self) -> None:
		...

	def addType(self, elt : LabelType) -> None:
		...

	def getHeight(self, elt : LabelType) -> coordType:
		...

	def getWidth(self, elt : LabelType) -> coordType:
		...

	def getX(self, elt : LabelType) -> coordType:
		...

	def getY(self, elt : LabelType) -> coordType:
		...

	def __assign__(self, rhs : EdgeLabel) -> EdgeLabel:
		...

	def __ior__(self, rhs : EdgeLabel) -> EdgeLabel:
		...

	def setEdge(self, e : edge) -> None:
		...

	def setHeight(self, elt : LabelType, h : coordType) -> None:
		...

	def setWidth(self, elt : LabelType, w : coordType) -> None:
		...

	def setX(self, elt : LabelType, x : coordType) -> None:
		...

	def setY(self, elt : LabelType, y : coordType) -> None:
		...

	def theEdge(self) -> edge:
		...

	@overload
	def usedLabel(self) -> int:
		...

	@overload
	def usedLabel(self, elt : LabelType) -> bool:
		...
