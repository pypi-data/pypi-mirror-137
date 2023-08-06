# file stubs/ogdf/MinSteinerTreeGoemans139/Main.py generated from classogdf_1_1_min_steiner_tree_goemans139_1_1_main
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
class Main(object):

	"""Class managing LP-based approximation."""

	# Finding full components

	# Preliminaries and preprocessing for the approximation algorithm

	def __init__(self, G : EdgeWeightedGraph[ T ], terminals : List[node], isTerminal : NodeArray[ bool ], restricted : int, use2approx : bool, separateCycles : bool, eps : float = 1e-8) -> None:
		"""Initialize all attributes, sort the terminal list."""
		...

	def __destruct__(self) -> None:
		...

	def getApproximation(self, finalSteinerTree : EdgeWeightedGraphCopy[ T ], rng : std.minstd_rand, doPreprocessing : bool = True) -> T:
		"""Obtain an (1.39+epsilon)-approximation based on the LP solution."""
		...
