# file stubs/ogdf/cluster_planarity/ChunkConnection.py generated from classogdf_1_1cluster__planarity_1_1_chunk_connection
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
class ChunkConnection(ogdf.cluster_planarity.BaseConstraint):

	def __init__(self, master : abacus.Master, chunk : ArrayBuffer[node], cochunk : ArrayBuffer[node]) -> None:
		...

	def __destruct__(self) -> None:
		...

	@overload
	def coeff(self, v : abacus.Variable) -> float:
		"""Returns the coefficient of the variablevin the constraint."""
		...

	@overload
	def coeff(self, n : NodePair) -> int:
		...

	@overload
	def coeff(self, v1 : node, v2 : node) -> int:
		...

	def printMe(self, out : std.ostream) -> None:
		...
