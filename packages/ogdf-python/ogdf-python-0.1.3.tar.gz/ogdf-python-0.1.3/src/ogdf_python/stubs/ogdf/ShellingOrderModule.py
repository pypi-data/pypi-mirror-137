# file stubs/ogdf/ShellingOrderModule.py generated from classogdf_1_1_shelling_order_module
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
class ShellingOrderModule(object):

	"""Base class for modules that compute a shelling order of a graph."""

	m_baseRatio : float = ...

	def __destruct__(self) -> None:
		...

	@overload
	def baseRatio(self) -> float:
		"""Returns the current setting of the optionbase ratio."""
		...

	@overload
	def baseRatio(self, x : float) -> None:
		"""Sets the optionbase ratiotox."""
		...

	def call(self, G : Graph, order : ShellingOrder, adj : adjEntry = None) -> None:
		"""Computes a shelling order of an embedded graph G such thatadjlies on the external face."""
		...

	def callLeftmost(self, G : Graph, order : ShellingOrder, adj : adjEntry = None) -> None:
		"""Computes a lefmost shelling order of an embedded graph G such thatadjlies on the external face."""
		...

	def doCall(self, G : Graph, adj : adjEntry, partition : List[ShellingOrderSet]) -> None:
		"""This pure virtual function does the actual computation."""
		...
