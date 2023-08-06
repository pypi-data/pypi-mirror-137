# file stubs/ogdf/SimDrawCreator.py generated from classogdf_1_1_sim_draw_creator
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
class SimDrawCreator(ogdf.SimDrawManipulatorModule):

	"""Creates variety of possibleSimDrawcreations."""

	def __init__(self, SD : SimDraw) -> None:
		"""constructor"""
		...

	def clearESG(self) -> None:
		"""clears edgeSubGraphs value"""
		...

	def createRandom(self, numberOfNodes : int, numberOfEdges : int, numberOfBasicGraphs : int) -> None:
		"""randomly creates a simdraw instance"""
		...

	def randomESG(self, graphNumber : int) -> None:
		"""randomly chose edgeSubGraphs value for graphNumber graphs"""
		...

	def randomESG2(self, doubleESGProbability : int = 50) -> None:
		"""randomly chose edgeSubGraphs value for two graphs"""
		...

	def randomESG3(self, doubleESGProbability : int = 50, tripleESGProbability : int = 25) -> None:
		"""randomly chose edgeSubGraphs value for three graphs"""
		...

	def readGraph(self, G : Graph) -> None:
		"""reads aGraph"""
		...

	@overload
	def SubGraphBits(self, e : edge) -> int:
		"""returns SubGraphBits from edge e"""
		...

	@overload
	def SubGraphBits(self, e : edge) -> int:
		"""returns SubGraphBits from edge e"""
		...
