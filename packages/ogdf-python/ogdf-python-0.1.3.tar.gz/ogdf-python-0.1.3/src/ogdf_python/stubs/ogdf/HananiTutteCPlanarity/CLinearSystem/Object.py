# file stubs/ogdf/HananiTutteCPlanarity/CLinearSystem/Object.py generated from structogdf_1_1_hanani_tutte_c_planarity_1_1_c_linear_system_1_1_object
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
class Object(object):

	m_c : cluster = ...

	m_c2 : cluster = ...

	m_e : edge = ...

	m_st : SubType = ...

	m_t : Type = ...

	m_v : node = ...

	@overload
	def __init__(self) -> None:
		...

	@overload
	def __init__(self, c : cluster) -> None:
		...

	@overload
	def __init__(self, c : cluster, c2 : cluster, e : edge) -> None:
		...

	@overload
	def __init__(self, e : edge) -> None:
		...

	@overload
	def __init__(self, v : node) -> None:
		...

	@overload
	def __init__(self, v : node, c : cluster, e : edge) -> None:
		...

	@overload
	def __init__(self, t : Type, st : SubType, c : cluster, e : edge) -> None:
		...

	def __lt__(self, other : Object) -> bool:
		...

	def __eq__(self, other : Object) -> bool:
		...
