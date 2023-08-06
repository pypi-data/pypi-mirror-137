# file stubs/ogdf/cluster_planarity/MinimalClusterConnection.py generated from classogdf_1_1cluster__planarity_1_1_minimal_cluster_connection
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
class MinimalClusterConnection(abacus.Constraint):

	def __init__(self, master : abacus.Master, edges : List[NodePair]) -> None:
		...

	def __destruct__(self) -> None:
		...

	def coeff(self, v : abacus.Variable) -> float:
		"""Returns the coefficient of the variablevin the constraint."""
		...
