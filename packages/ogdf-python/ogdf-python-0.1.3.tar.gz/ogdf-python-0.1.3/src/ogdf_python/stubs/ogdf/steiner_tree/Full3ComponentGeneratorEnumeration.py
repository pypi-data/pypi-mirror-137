# file stubs/ogdf/steiner_tree/Full3ComponentGeneratorEnumeration.py generated from classogdf_1_1steiner__tree_1_1_full3_component_generator_enumeration
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
T = TypeVar('T')

class Full3ComponentGeneratorEnumeration(ogdf.steiner_tree.Full3ComponentGeneratorModule[ T ], Generic[T]):

	"""Full 3-component generation using enumeration."""

	def call(self, G : EdgeWeightedGraph[ T ], terminals : List[node], isTerminal : NodeArray[ bool ], distance : NodeArray[NodeArray[ T ]], pred : NodeArray[NodeArray[edge]], generateFunction : Callable) -> None:
		"""Generate full components and callgenerateFunctionfor each full component."""
		...
