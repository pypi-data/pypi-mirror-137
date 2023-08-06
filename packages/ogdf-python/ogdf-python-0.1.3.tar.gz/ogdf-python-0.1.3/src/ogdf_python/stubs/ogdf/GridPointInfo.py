# file stubs/ogdf/GridPointInfo.py generated from structogdf_1_1_grid_point_info
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
class GridPointInfo(object):

	m_e : edge = ...

	m_v : node = ...

	@overload
	def __init__(self) -> None:
		...

	@overload
	def __init__(self, e : edge) -> None:
		...

	@overload
	def __init__(self, v : node) -> None:
		...

	def __ne__(self, i : GridPointInfo) -> bool:
		...

	def __eq__(self, i : GridPointInfo) -> bool:
		...
