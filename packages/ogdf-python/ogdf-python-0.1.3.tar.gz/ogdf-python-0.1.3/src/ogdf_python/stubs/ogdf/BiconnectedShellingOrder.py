# file stubs/ogdf/BiconnectedShellingOrder.py generated from classogdf_1_1_biconnected_shelling_order
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
class BiconnectedShellingOrder(ogdf.ShellingOrderModule):

	"""Computation of the shelling order for biconnected graphs."""

	def __init__(self) -> None:
		"""Creates a biconnected shelling order module."""
		...

	def doCall(self, G : Graph, adj : adjEntry, partition : List[ShellingOrderSet]) -> None:
		"""The actual implementation of the module call."""
		...
