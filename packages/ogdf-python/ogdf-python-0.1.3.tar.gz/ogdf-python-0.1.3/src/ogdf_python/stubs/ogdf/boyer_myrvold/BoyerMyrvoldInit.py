# file stubs/ogdf/boyer_myrvold/BoyerMyrvoldInit.py generated from classogdf_1_1boyer__myrvold_1_1_boyer_myrvold_init
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
class BoyerMyrvoldInit(object):

	"""This class is used in the Boyer-Myrvold planarity test for preprocessing purposes."""

	def __init__(self, pBM : BoyerMyrvoldPlanar) -> None:
		"""Constructor, the parameterBoyerMyrvoldPlanaris needed."""
		...

	def __destruct__(self) -> None:
		"""Destructor."""
		...

	def computeDFS(self) -> None:
		"""Creates the DFSTree."""
		...

	def computeDFSChildLists(self) -> None:
		"""Computes the list of separated DFS children for all nodes."""
		...

	def computeLowPoints(self) -> None:
		"""Computes lowpoint, highestSubtreeDFI and links virtual to nonvirtual vertices."""
		...

	def __assign__(self, _ : BoyerMyrvoldInit) -> BoyerMyrvoldInit:
		"""Assignment operator is undefined!"""
		...
