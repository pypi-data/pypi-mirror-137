# file stubs/ogdf/ConnectivityTester.py generated from classogdf_1_1_connectivity_tester
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
class ConnectivityTester(object):

	"""Naive implementation for testing the connectivity of a graph."""

	@overload
	def __init__(self, nodeConnectivity : bool = True, directed : bool = False) -> None:
		"""Initializes a new connectivity tester usingogdf::MaxFlowGoldbergTarjan."""
		...

	@overload
	def __init__(self, flowAlgo : MaxFlowModule[  int ], nodeConnectivity : bool = True, directed : bool = False) -> None:
		"""Initializes a new onnectivity tester using a customogdf::MaxFlowModule."""
		...

	def __destruct__(self) -> None:
		"""Destroys the connectivity tester and frees allocated memory."""
		...

	@overload
	def computeConnectivity(self, graph : Graph, v : node, u : node) -> int:
		"""Computes the connectivity of two nodes."""
		...

	@overload
	def computeConnectivity(self, graph : Graph, result : NodeArray[NodeArray[  int ]]) -> int:
		"""Computes the connectivity of all nodes of the provided graph."""
		...
