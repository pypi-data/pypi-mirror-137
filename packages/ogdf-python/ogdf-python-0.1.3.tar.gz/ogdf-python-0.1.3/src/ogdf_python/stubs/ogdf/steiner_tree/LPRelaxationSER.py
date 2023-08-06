# file stubs/ogdf/steiner_tree/LPRelaxationSER.py generated from classogdf_1_1steiner__tree_1_1_l_p_relaxation_s_e_r
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
T = TypeVar('T')

class LPRelaxationSER(Generic[T]):

	"""Class managing the component-based subtour elimination LP relaxation for the Steiner tree problem and its solving."""

	def __init__(self, G : EdgeWeightedGraph[ T ], terminals : List[node], isTerminal : NodeArray[ bool ], fullCompStore : FullComponentWithExtraStore[ T, float ], upperBound : T = 0, cliqueSize : int = 0, eps : float = 1e-8) -> None:
		"""Initialize the LP."""
		...

	def __destruct__(self) -> None:
		...

	def solve(self) -> bool:
		"""Solve the LP. The solution will be written to the extra data of the full component store."""
		...
