# file stubs/ogdf/Stroke.py generated from structogdf_1_1_stroke
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
class Stroke(object):

	"""Properties of strokes."""

	#: line-cap of the stroke
	m_cap : StrokeLineCap = ...

	#: stroke color
	m_color : Color = ...

	#: line-join of the stroke
	m_join : StrokeLineJoin = ...

	#: stroke type (e.g.
	m_type : StrokeType = ...

	#: stroke width
	m_width : float = ...

	@overload
	def __init__(self) -> None:
		...

	@overload
	def __init__(self, c : Color) -> None:
		...
