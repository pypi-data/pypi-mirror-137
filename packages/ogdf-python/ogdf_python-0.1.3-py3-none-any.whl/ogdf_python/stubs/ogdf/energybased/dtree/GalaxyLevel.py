# file stubs/ogdf/energybased/dtree/GalaxyLevel.py generated from classogdf_1_1energybased_1_1dtree_1_1_galaxy_level
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
class GalaxyLevel(object):

	"""Simple implementation of the slightly modified version of Hachul by Gronemann."""

	def __init__(self, graph : Graph) -> None:
		"""constructor for the finest level i.e. the original graph"""
		...

	def __destruct__(self) -> None:
		"""destructor, deletes this level and all subsequent i.e coarser ones"""
		...

	def buildLevelsUntil(self, maxNumNodes : int) -> GalaxyLevel:
		"""Builds all levels until the graph has less thanmaxNumNodes."""
		...

	def edgeWeight(self, e : edge) -> float:
		"""returns the edge weight of e"""
		...

	def graph(self) -> Graph:
		"""returns the graph"""
		...

	def isCoarsestLevel(self) -> bool:
		"""returns true if this is the coarsest level"""
		...

	def isFinestLevel(self) -> bool:
		"""returns true if this is the level of the original graph"""
		...

	def nextCoarser(self) -> GalaxyLevel:
		"""return the next coarser one"""
		...

	def nextFiner(self) -> GalaxyLevel:
		"""return the next finer one"""
		...

	def parent(self, v : node) -> node:
		"""returns the parent node of a node on the coarser level"""
		...

	def setEdgeWeight(self, e : edge, weight : float) -> None:
		"""returns the edge weight of e"""
		...

	def setWeight(self, v : node, weight : float) -> None:
		"""returns the weight of a node"""
		...

	def weight(self, v : node) -> float:
		"""returns the weight of a node"""
		...
