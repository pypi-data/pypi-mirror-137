# file stubs/ogdf/MixedModelBase.py generated from classogdf_1_1_mixed_model_base
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
class MixedModelBase(object):

	def printMMOrder(self, os : std.ostream) -> None:
		"""Functions for debugging output."""
		...

	def printInOutPoints(self, os : std.ostream) -> None:
		...

	def print(self, os : std.ostream, iop : InOutPoint) -> None:
		...

	def printNodeCoords(self, os : std.ostream) -> None:
		...

	def __init__(self, PG : PlanRep, gridLayout : GridLayout) -> None:
		...

	def __destruct__(self) -> None:
		...

	def assignIopCoords(self) -> None:
		"""Computes the relative coordinates of the in- and outpoints, incl. height(v), depth(v)."""
		...

	def computeOrder(self, augmenter : AugmentationModule, pEmbedder : EmbedderModule, adjExternal : adjEntry, compOrder : ShellingOrderModule) -> None:
		"""Computes the ordered partition (incl.m_leftOp[k], em_rightOp[k]) and constructs the in- and outpoint lists."""
		...

	def computeXCoords(self) -> None:
		"""Computes the absolute x-coordinates x[v] of all nodes in the ordering, furthermore dyla[k] and dyra[k] (used by compute_y_coordinates)"""
		...

	def computeYCoords(self) -> None:
		"""Computes the absolute y-coordinates y[v] of all nodes in the ordering."""
		...

	def __assign__(self, _ : MixedModelBase) -> MixedModelBase:
		...

	def placeNodes(self) -> None:
		"""Implements the placement step. Computes x[v] and y[v]."""
		...

	def postprocessing1(self) -> None:
		"""Tries to reduce the number of bends by changing the outpoints of nodes with indeg and outdeg 2."""
		...

	def postprocessing2(self) -> None:
		"""Tries to reduce the number of bends by moving degree-2 nodes on bend points."""
		...

	def setBends(self) -> None:
		"""Assigns polylines to edges of the original graph and computes the x- and y-coordinates of deg-1-nodes not in the ordering."""
		...
