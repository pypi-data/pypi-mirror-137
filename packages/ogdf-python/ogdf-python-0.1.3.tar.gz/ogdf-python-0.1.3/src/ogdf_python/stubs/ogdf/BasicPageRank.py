# file stubs/ogdf/BasicPageRank.py generated from classogdf_1_1_basic_page_rank
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
class BasicPageRank(object):

	"""Basic page rank calculation."""

	def __init__(self) -> None:
		...

	def call(self, graph : Graph, edgeWeight : EdgeArray[ float ], pageRankResult : NodeArray[ float ]) -> None:
		"""main algorithm call"""
		...

	def dampingFactor(self) -> float:
		"""returns the damping factor for each iteration (default is 0.85)"""
		...

	def initDefaultOptions(self) -> None:
		"""sets the default options."""
		...

	def maxNumIterations(self) -> int:
		"""the maximum number of iterations (default is 1000)"""
		...

	def setDampingFactor(self, dampingFactor : float) -> None:
		"""sets the damping factor for each iteration (default is 0.85)"""
		...

	def setMaxNumIterations(self, maxNumIterations : int) -> None:
		"""sets the maximum number of iterations (default is 1000)"""
		...

	def setThreshold(self, t : float) -> None:
		"""sets the threshold to t. See threshold for more information"""
		...

	def threshold(self) -> float:
		"""returns the threshold/epsilon."""
		...
