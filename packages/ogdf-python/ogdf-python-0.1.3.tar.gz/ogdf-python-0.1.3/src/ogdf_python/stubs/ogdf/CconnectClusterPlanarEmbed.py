# file stubs/ogdf/CconnectClusterPlanarEmbed.py generated from classogdf_1_1_cconnect_cluster_planar_embed
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
class CconnectClusterPlanarEmbed(object):

	"""C-planarity test and embedding by Cohen, Feng and Eades."""

	# private member variables for testing a cluster graph

	# private members for handling parallel edges

	# private member variables for embedding a cluster graph

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

	def embed(self, C : ClusterGraph, G : Graph) -> bool:
		"""Tests if a clustered graph (C,G) is C-planar and embeds it."""
		...

	def errCode(self) -> ErrorCode:
		...
