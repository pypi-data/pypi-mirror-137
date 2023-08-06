# file stubs/ogdf/ELabelInterface.py generated from classogdf_1_1_e_label_interface
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
coordType = TypeVar('coordType')

class ELabelInterface(Generic[coordType]):

	@overload
	def __init__(self, uml : GraphAttributes) -> None:
		...

	@overload
	def __init__(self, pru : PlanRepUML) -> None:
		...

	def addLabel(self, e : edge, el : EdgeLabel[ coordType ]) -> None:
		...

	def distDefault(self) -> coordType:
		...

	def getHeight(self, e : edge, elt : LabelType) -> coordType:
		...

	def getLabel(self, e : edge) -> EdgeLabel[ coordType ]:
		...

	def getWidth(self, e : edge, elt : LabelType) -> coordType:
		...

	def graph(self) -> GraphAttributes:
		...

	def minFeatDist(self) -> coordType:
		...

	def setLabel(self, e : edge, el : EdgeLabel[ coordType ]) -> None:
		...
