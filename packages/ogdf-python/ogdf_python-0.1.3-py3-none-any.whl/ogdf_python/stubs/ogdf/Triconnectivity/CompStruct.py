# file stubs/ogdf/Triconnectivity/CompStruct.py generated from structogdf_1_1_triconnectivity_1_1_comp_struct
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
class CompStruct(object):

	"""representation of a component"""

	m_edges : List[edge] = ...

	m_type : CompType = ...

	def finishTricOrPoly(self, e : edge) -> None:
		...

	def __lshift__(self, e : edge) -> CompStruct:
		...
