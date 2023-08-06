# file stubs/ogdf/Fill.py generated from structogdf_1_1_fill
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
class Fill(object):

	"""Properties of fills."""

	#: background color of fill pattern
	m_bgColor : Color = ...

	#: fill color
	m_color : Color = ...

	#: fill pattern
	m_pattern : FillPattern = ...

	@overload
	def __init__(self) -> None:
		...

	@overload
	def __init__(self, c : Color) -> None:
		...

	@overload
	def __init__(self, c : Color, bgColor : Color, pattern : FillPattern) -> None:
		...

	@overload
	def __init__(self, c : Color, pattern : FillPattern) -> None:
		...
