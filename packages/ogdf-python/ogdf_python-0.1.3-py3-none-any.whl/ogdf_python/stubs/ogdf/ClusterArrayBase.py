# file stubs/ogdf/ClusterArrayBase.py generated from classogdf_1_1_cluster_array_base
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
class ClusterArrayBase(object):

	"""Abstract base class for cluster arrays."""

	#: The associated cluster graph.
	m_pClusterGraph : ClusterGraph = ...

	@overload
	def __init__(self) -> None:
		"""Initializes a cluster array not associated with a cluster graph."""
		...

	@overload
	def __init__(self, base : ClusterArrayBase) -> None:
		"""Moves cluster arraybaseto this cluster array."""
		...

	@overload
	def __init__(self, pC : ClusterGraph) -> None:
		"""Initializes a cluster array associated withpC."""
		...

	def __destruct__(self) -> None:
		...

	def disconnect(self) -> None:
		"""Virtual function called when array is disconnected from the cluster graph."""
		...

	def enlargeTable(self, newTableSize : int) -> None:
		"""Virtual function called when table size has to be enlarged."""
		...

	def moveRegister(self, base : ClusterArrayBase) -> None:
		"""Moves array registration frombaseto this array."""
		...

	def reinit(self, initTableSize : int) -> None:
		"""Virtual function called when table has to be reinitialized."""
		...

	def reregister(self, pC : ClusterGraph) -> None:
		"""Associates the array with a new cluster graph."""
		...
