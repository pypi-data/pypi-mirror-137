# file stubs/ogdf/CliqueFinderHeuristic.py generated from classogdf_1_1_clique_finder_heuristic
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
class CliqueFinderHeuristic(ogdf.CliqueFinderModule):

	"""Finds cliques and dense subgraphs using a heuristic."""

	def __init__(self) -> None:
		"""Creates aCliqueFinderHeuristic."""
		...

	def setDensity(self, density : float) -> None:
		"""Sets the density needed for subgraphs to be detected."""
		...

	def setPostProcessing(self, postProcess : bool) -> None:
		"""Sets whether postprocessing should be activated."""
		...

	def allAdjacent(self, v : node, vList : List[node]) -> bool:
		"""Checks whethervis adjacent to (at leastm_densitytimes) all nodes invList."""
		...

	def doCall(self) -> None:
		"""Find cliques inm_pCopy."""
		...

	def evaluate(self, v : node) -> int:
		"""Evaluatesvinm_pCopyheuristically concerning its qualification as a clique start node."""
		...

	def findClique(self, v : node, neighbours : List[node]) -> None:
		"""Searches for a clique/dense subgraph around nodevin listneighbours."""
		...

	def postProcessCliques(self, cliqueList : List[List[node]  ]) -> None:
		"""If postprocessing is activated, use the result of the first phase and revisit cliques that are too small."""
		...

	def preProcess(self) -> None:
		"""Deletes all nodes fromm_pCopywith degree <m_density*m_minDegreein O(n+m)."""
		...
