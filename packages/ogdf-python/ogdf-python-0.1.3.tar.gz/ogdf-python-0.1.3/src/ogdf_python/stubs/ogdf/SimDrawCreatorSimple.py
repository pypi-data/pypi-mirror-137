# file stubs/ogdf/SimDrawCreatorSimple.py generated from classogdf_1_1_sim_draw_creator_simple
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
class SimDrawCreatorSimple(ogdf.SimDrawCreator):

	"""Offers predefinedSimDrawcreations."""

	def __init__(self, SD : SimDraw) -> None:
		"""constructor"""
		...

	def createExpo(self, n : int) -> None:
		"""creates simultaneously planar simultaneous graph with n+1 basic graphs."""
		...

	def createK5_EK04(self) -> None:
		"""creates K5 instance from Erten and Kobourov (GD'04)"""
		...

	def createK5_GJPSS06(self) -> None:
		"""creates K5 instance from Gassner et al. (WG'06)"""
		...

	def createKrat98(self, N : int, nodeNumber : int) -> None:
		"""creates instance from Kratochvil (GD'98)"""
		...

	def createOuterplanar_BCDEEIKLM03(self) -> None:
		"""creates instance of two outerplanar graphs from Brass et al. (WADS'03)"""
		...

	def createPathPlanar_EK04(self) -> None:
		"""creates instance of a path and a planar graph from Erten and Kobourov (GD'04)"""
		...

	def createTrees_GKV05(self, n : int) -> None:
		"""creates pair-of-tree instance from Geyer, Kaufmann, Vrto (GD'05)"""
		...

	def createWheel(self, numberOfParallels : int, numberOfbasic : int) -> None:
		"""creates instance with numberofBasic*2 outer, numberOfParallels*numberOfBasic inner Nodes and one Root."""
		...
