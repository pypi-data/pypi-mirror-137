# file stubs/ogdf/MaxFlowModule.py generated from classogdf_1_1_max_flow_module
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
T = TypeVar('T')

class MaxFlowModule(Generic[T]):

	#: Pointer to the given capacity array.
	m_cap : EdgeArray[ T ] = ...

	#: Pointer to the usedEpsilonTest.
	m_et : EpsilonTest = ...

	#: Pointer to (extern) flow array.
	m_flow : EdgeArray[ T ] = ...

	#: Pointer to the given graph.
	m_G : Graph = ...

	#: Pointer to the source node.
	m_s : node = ...

	#: Pointer to the sink node.
	m_t : node = ...

	@overload
	def __init__(self) -> None:
		"""Empty Constructor."""
		...

	@overload
	def __init__(self, graph : Graph, flow : EdgeArray[ T ] = None) -> None:
		"""Constructor that calls init."""
		...

	def __destruct__(self) -> None:
		"""Destructor that deletes m_flow if it is an internal flow array."""
		...

	def computeFlow(self, cap : EdgeArray[ T ], s : node, t : node, flow : EdgeArray[ T ]) -> T:
		"""Only a shortcut for computeValue and computeFlowAfterValue."""
		...

	@overload
	def computeFlowAfterValue(self) -> None:
		"""Compute the flow itself after the flow value is already computed. Only used in algorithms with 2 phases. The flow is stored in the array that the user gave in the constructor."""
		...

	@overload
	def computeFlowAfterValue(self, flow : EdgeArray[ T ]) -> None:
		"""Compute the flow itself after the flow value is already computed. Only used in algorithms with 2 phases. The flow is stored in the parameterflow."""
		...

	def computeValue(self, cap : EdgeArray[ T ], s : node, t : node) -> T:
		"""Compute only the value of the flow."""
		...

	def init(self, graph : Graph, flow : EdgeArray[ T ] = None) -> None:
		"""Initialize the problem with a graph and optional flow array. If noflowarray is given, a new ("internal") array will be created. If aflowarray is given, the algorithm uses this "external" array."""
		...

	def isFeasibleInstance(self) -> bool:
		"""Return whether the instance is feasible, i.e. the capacities are non-negative."""
		...

	def useEpsilonTest(self, eps : float) -> None:
		"""Change the usedEpsilonTestfrom StandardEpsilonTest to a user givenEpsilonTest."""
		...
