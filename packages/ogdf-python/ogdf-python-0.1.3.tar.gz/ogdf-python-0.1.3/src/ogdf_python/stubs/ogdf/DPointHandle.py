# file stubs/ogdf/DPointHandle.py generated from classogdf_1_1_d_point_handle
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
class DPointHandle(object):

	@overload
	def __init__(self) -> None:
		...

	@overload
	def __init__(self, p : DPointHandle) -> None:
		...

	@overload
	def __init__(self, x : float, y : float) -> None:
		...

	def __destruct__(self) -> None:
		...

	def id(self) -> int:
		...

	def identical(self, p : DPointHandle) -> bool:
		...

	def __ne__(self, p : DPointHandle) -> bool:
		...

	def __lt__(self, p : DPointHandle) -> bool:
		...

	def __assign__(self, p : DPointHandle) -> DPointHandle:
		...

	def __eq__(self, p : DPointHandle) -> bool:
		...

	def __gt__(self, p : DPointHandle) -> bool:
		...

	def xcoord(self) -> float:
		...

	def ycoord(self) -> float:
		...
