# file stubs/ogdf/SimDrawManipulatorModule.py generated from classogdf_1_1_sim_draw_manipulator_module
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
class SimDrawManipulatorModule(object):

	"""Interface for simdraw manipulators."""

	#: pointer to current graph
	m_G : Graph = ...

	#: pointer to current graphattributes
	m_GA : GraphAttributes = ...

	#: pointer to current simdraw instance
	m_SD : SimDraw = ...

	@overload
	def __init__(self) -> None:
		"""default constructor"""
		...

	@overload
	def __init__(self, SD : SimDraw) -> None:
		"""constructor"""
		...

	def constSimDraw(self) -> SimDraw:
		"""returns base instance"""
		...

	def init(self, SD : SimDraw) -> None:
		"""initializing base instance"""
		...
