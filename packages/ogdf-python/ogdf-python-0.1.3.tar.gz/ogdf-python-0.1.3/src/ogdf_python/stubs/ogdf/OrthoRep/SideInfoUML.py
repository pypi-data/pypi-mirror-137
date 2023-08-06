# file stubs/ogdf/OrthoRep/SideInfoUML.py generated from structogdf_1_1_ortho_rep_1_1_side_info_u_m_l
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
class SideInfoUML(object):

	"""Information about a side of a vertex in UML diagrams."""

	m_adjGen : adjEntry = ...

	m_nAttached : int = ...

	def __init__(self) -> None:
		...

	def totalAttached(self) -> int:
		...
