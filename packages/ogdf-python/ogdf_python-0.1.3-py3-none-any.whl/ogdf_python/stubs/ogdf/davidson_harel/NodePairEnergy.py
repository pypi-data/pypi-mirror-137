# file stubs/ogdf/davidson_harel/NodePairEnergy.py generated from classogdf_1_1davidson__harel_1_1_node_pair_energy
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
class NodePairEnergy(ogdf.davidson_harel.EnergyFunction):

	def __init__(self, energyname : str, AG : GraphAttributes) -> None:
		...

	def __destruct__(self) -> None:
		...

	def computeEnergy(self) -> None:
		"""computes energy for the layout at the beginning of the optimization process"""
		...

	def adjacent(self, v : node, w : node) -> bool:
		"""returns true in constant time if two vertices are adjacent."""
		...

	def computeCoordEnergy(self, _ : node, _ : node, _ : DPoint, _ : DPoint) -> float:
		"""Computes the energy stored by a pair of vertices at the given positions."""
		...

	def nodeNum(self, v : node) -> int:
		"""Returns the internal number given to each vertex."""
		...

	def shape(self, v : node) -> DIntersectableRect:
		"""Returns the shape of a vertexvas aDIntersectableRect."""
		...
