# file stubs/ogdf/CconnectClusterPlanar.py generated from classogdf_1_1_cconnect_cluster_planar
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
class CconnectClusterPlanar(object):

	"""C-planarity test by Cohen, Feng and Eades."""

	class ErrorCode(enum.Enum):

		none = enum.auto()

		nonConnected = enum.auto()

		nonCConnected = enum.auto()

		nonPlanar = enum.auto()

		nonCPlanar = enum.auto()

	def __init__(self) -> None:
		"""Constructor."""
		...

	def __destruct__(self) -> None:
		"""Destructor."""
		...

	def call(self, C : ClusterGraph) -> bool:
		"""Tests if a cluster graph is c-planar."""
		...

	def errCode(self) -> ErrorCode:
		...
