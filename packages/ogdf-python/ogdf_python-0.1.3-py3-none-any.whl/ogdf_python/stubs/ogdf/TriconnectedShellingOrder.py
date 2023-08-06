# file stubs/ogdf/TriconnectedShellingOrder.py generated from classogdf_1_1_triconnected_shelling_order
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
class TriconnectedShellingOrder(ogdf.ShellingOrderModule):

	"""Computation of a shelling order for a triconnected and simple (no multi-edges, no self-loops) planar graph."""

	def __init__(self) -> None:
		...

	def doCall(self, G : Graph, adj : adjEntry, partition : List[ShellingOrderSet]) -> None:
		"""This pure virtual function does the actual computation."""
		...
