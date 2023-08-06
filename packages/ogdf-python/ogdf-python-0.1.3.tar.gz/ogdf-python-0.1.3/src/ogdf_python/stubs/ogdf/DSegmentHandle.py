# file stubs/ogdf/DSegmentHandle.py generated from classogdf_1_1_d_segment_handle
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
class DSegmentHandle(object):

	@overload
	def __init__(self) -> None:
		...

	@overload
	def __init__(self, p1 : DPointHandle, p2 : DPointHandle) -> None:
		...

	@overload
	def __init__(self, seg : DSegmentHandle) -> None:
		...

	@overload
	def __init__(self, x1 : float, y1 : float, x2 : float, y2 : float) -> None:
		...

	def __destruct__(self) -> None:
		...

	def dx(self) -> float:
		...

	def dy(self) -> float:
		...

	def end(self) -> DPointHandle:
		...

	def id(self) -> int:
		...

	def identical(self, seg : DSegmentHandle) -> bool:
		...

	def intersectionOfLines(self, line : DSegmentHandle, inter : DPointHandle) -> bool:
		...

	def isVertical(self) -> bool:
		...

	def __ne__(self, seg : DSegmentHandle) -> bool:
		...

	def __assign__(self, seg : DSegmentHandle) -> DSegmentHandle:
		...

	def __eq__(self, seg : DSegmentHandle) -> bool:
		...

	def slope(self) -> float:
		...

	def start(self) -> DPointHandle:
		...

	def yAbs(self) -> float:
		...
