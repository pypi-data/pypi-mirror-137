# file stubs/ogdf/CliqueFinderModule.py generated from classogdf_1_1_clique_finder_module
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
class CliqueFinderModule(object):

	"""Finds cliques."""

	# Parameter Setters

	def setMinSize(self, i : int) -> None:
		"""Sets the minimum size of a clique."""
		...

	# Helper Functions

	def cliqueListToNumber(self, G : Graph, cliqueLists : List[List[node]  ], cliqueNumber : NodeArray[  int ]) -> None:
		"""Uses a list of cliques to get the clique number of each node."""
		...

	def cliqueNumberToList(self, G : Graph, cliqueNumber : NodeArray[  int ], cliqueLists : List[List[node]  ]) -> None:
		"""Uses the clique number for each node to create a list of cliques."""
		...

	def cliqueGraphAttributes(self, G : Graph, cliqueNumber : NodeArray[  int ], GA : GraphAttributes) -> None:
		"""Labels and colors nodes in the givenGraphAttributesaccording to their clique number."""
		...

	def cliqueOK(self, G : Graph, clique : List[node], density : float = 1.0) -> bool:
		"""Checks whether density times the number of possible edges exist between clique members."""
		...

	#: The clique number for each node inm_pCopy.
	m_copyCliqueNumber : NodeArray[  int ] = ...

	#: Minimum degree of the nodes in a found clique.
	m_minDegree : int = ...

	#: Copy ofm_pGraphwithout self-loops and multi-edges.
	m_pCopy : GraphCopy = ...

	def __init__(self) -> None:
		"""Creates aCliqueFinderModule."""
		...

	def __destruct__(self) -> None:
		...

	@overload
	def call(self, G : Graph, cliqueLists : List[List[node]  ]) -> None:
		"""Searches for cliques and returns the list of cliques."""
		...

	@overload
	def call(self, G : Graph, cliqueNumber : NodeArray[  int ]) -> None:
		"""Searches for cliques and sets the clique index number for each node."""
		...

	def doCall(self) -> None:
		"""Find cliques inm_pCopy."""
		...
