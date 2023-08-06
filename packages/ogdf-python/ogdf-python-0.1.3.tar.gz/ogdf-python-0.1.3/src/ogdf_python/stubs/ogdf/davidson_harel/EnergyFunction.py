# file stubs/ogdf/davidson_harel/EnergyFunction.py generated from classogdf_1_1davidson__harel_1_1_energy_function
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
class EnergyFunction(object):

	"""The interface for energy functions for the Davidson Harel graph drawing method."""

	#: the energy of the layout if the candidate layout is chosen
	m_candidateEnergy : float = ...

	#: energy of the current layout
	m_energy : float = ...

	#: the graph that should be drawn
	m_G : Graph = ...

	#: name of the energy function
	m_name : str = ...

	def __init__(self, funcname : str, AG : GraphAttributes) -> None:
		"""Initializes data dtructures to speed up later computations."""
		...

	def __destruct__(self) -> None:
		...

	def candidateTaken(self) -> None:
		"""Changes m_currentX and m_currentY by setting the position of m_testNode to m_testX and m_testY. Sets m_energy to m_candidateEnergy. Computes the energy of the layout stored in AG."""
		...

	def computeCandidateEnergy(self, v : node, newPos : DPoint) -> float:
		"""sets m_testNode, m_testX and m_testY and computes the energy for the new configuration (vertex v moves to newPos)"""
		...

	def computeEnergy(self) -> None:
		"""computes energy for the layout at the beginning of the optimization process"""
		...

	def energy(self) -> float:
		...

	def getName(self) -> str:
		"""prints the name of the energy function"""
		...

	def compCandEnergy(self) -> None:
		"""computes the energy if m_testNode changes position to m_testX and m_testY, sets the value of m_candidateEnergy."""
		...

	def currentPos(self, v : node) -> DPoint:
		"""returns the current position of vertex v"""
		...

	def internalCandidateTaken(self) -> None:
		"""changes the data of a specific energy function if the candidate was taken"""
		...

	def testNode(self) -> node:
		"""returns the vertex that is under consideration in the current step"""
		...

	def testPos(self) -> DPoint:
		"""returns candidate position for the node to be moved"""
		...
