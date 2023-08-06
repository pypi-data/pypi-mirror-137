# file stubs/ogdf/OrthoRep/VertexInfoUML.py generated from structogdf_1_1_ortho_rep_1_1_vertex_info_u_m_l
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
class VertexInfoUML(object):

	"""Further information about the cages of vertices in UML diagrams."""

	m_corner : adjEntry = ...

	m_side : SideInfoUML = ...

	def __init__(self) -> None:
		...
