# file stubs/ogdf/SimDrawCaller.py generated from classogdf_1_1_sim_draw_caller
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
class SimDrawCaller(ogdf.SimDrawManipulatorModule):

	"""Calls modified algorithms for simdraw instances."""

	def __init__(self, SD : SimDraw) -> None:
		"""constructor"""
		...

	def callPlanarizationLayout(self) -> None:
		"""runs UMLPlanarizationLayout with modified inserter"""
		...

	def callSubgraphPlanarizer(self, cc : int = 0, numberOfPermutations : int = 1) -> int:
		"""runsSubgraphPlanarizerwith modified inserter"""
		...

	def callSugiyamaLayout(self) -> None:
		"""runsSugiyamaLayoutwith modifiedSplitHeuristic"""
		...
