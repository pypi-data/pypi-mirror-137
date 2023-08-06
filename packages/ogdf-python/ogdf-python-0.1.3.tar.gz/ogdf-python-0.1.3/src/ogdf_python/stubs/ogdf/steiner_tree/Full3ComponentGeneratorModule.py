# file stubs/ogdf/steiner_tree/Full3ComponentGeneratorModule.py generated from classogdf_1_1steiner__tree_1_1_full3_component_generator_module
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
T = TypeVar('T')

class Full3ComponentGeneratorModule(Generic[T]):

	"""Interface for full 3-component generation including auxiliary functions."""

	def __init__(self) -> None:
		...

	def __destruct__(self) -> None:
		...

	def call(self, G : EdgeWeightedGraph[ T ], terminals : List[node], isTerminal : NodeArray[ bool ], distance : NodeArray[NodeArray[ T ]], pred : NodeArray[NodeArray[edge]], generateFunction : Callable) -> None:
		"""Generate full components and callgenerateFunctionfor each full component."""
		...

	def checkAndGenerateFunction(self, u : node, v : node, w : node, center : node, minCost : T, pred : NodeArray[NodeArray[edge]], isTerminal : NodeArray[ bool ], generateFunction : Callable) -> None:
		...

	def forAllTerminalTriples(self, terminals : List[node], distance : NodeArray[NodeArray[ T ]], func : Callable) -> None:
		...

	def updateBestCenter(self, x : node, center : node, minCost : T, dist1 : NodeArray[ T ], dist2 : NodeArray[ T ], dist3 : NodeArray[ T ]) -> None:
		"""Update center node if it is the best so far."""
		...
