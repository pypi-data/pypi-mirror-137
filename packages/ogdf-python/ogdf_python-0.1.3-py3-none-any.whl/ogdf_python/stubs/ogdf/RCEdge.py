# file stubs/ogdf/RCEdge.py generated from structogdf_1_1_r_c_edge
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
class RCEdge(object):

	m_cr : RCCrossings = ...

	m_crReverse : RCCrossings = ...

	m_src : node = ...

	m_tgt : node = ...

	@overload
	def __init__(self) -> None:
		...

	@overload
	def __init__(self, src : node, tgt : node, cr : RCCrossings, crReverse : RCCrossings) -> None:
		...

	def weight(self) -> RCCrossings:
		...
