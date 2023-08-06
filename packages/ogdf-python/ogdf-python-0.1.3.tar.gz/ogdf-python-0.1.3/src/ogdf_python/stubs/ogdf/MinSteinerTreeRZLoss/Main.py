# file stubs/ogdf/MinSteinerTreeRZLoss/Main.py generated from classogdf_1_1_min_steiner_tree_r_z_loss_1_1_main
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
class Main(object):

	# Finding full components

	def __init__(self, G : EdgeWeightedGraph[ T ], terminals : List[node], isTerminal : NodeArray[ bool ], restricted : int) -> None:
		...

	def getApproximation(self, finalSteinerTree : EdgeWeightedGraphCopy[ T ]) -> T:
		...

	def numberOfComponentLookUps(self) -> int:
		"""Returns the number of components lookups during execution time."""
		...

	def numberOfContractedComponents(self) -> int:
		"""Returns the number of contracted components."""
		...

	def numberOfGeneratedComponents(self) -> int:
		"""Returns the number of generated components."""
		...
