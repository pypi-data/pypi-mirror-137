# file stubs/ogdf/steiner_tree/__init__.py generated from namespaceogdf_1_1steiner__tree
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
T = TypeVar('T')

class steiner_tree(object):

	def buildHeaviestEdgeInComponentTree(self, inputTree : EdgeWeightedGraphCopy[ T ], externalNodes : NodeArray[node], treeEdge : NodeArray[edge], outputTree : Graph) -> node:
		"""Given an edge-weighted tree, builds an auxiliary arborescence where each arc of the input tree is a node in the arborescence."""
		...

	def constructTerminalSpanningTreeUsingVoronoiRegions(self, terminalSpanningTree : EdgeWeightedGraphCopy[ T ], graph : EdgeWeightedGraph[ T ], terminals : List[node]) -> T:
		...

	@overload
	def contractTripleInSteinerTree(self, t : Triple[ T ], st : EdgeWeightedGraphCopy[ T ], e0 : edge, e1 : edge, e2 : edge) -> None:
		...

	@overload
	def contractTripleInSteinerTree(self, t : Triple[ T ], st : EdgeWeightedGraphCopy[ T ], save0 : edge, save1 : edge, save2 : edge, ne0 : edge, ne1 : edge) -> None:
		"""Updates the Steiner tree by deleting save edges, removing all direct connections between the terminals of the contracted triple and connecting them through 0-cost edges."""
		...

	def obtainFinalSteinerTree(self, G : EdgeWeightedGraph[ T ], isTerminal : NodeArray[ bool ], isOriginalTerminal : NodeArray[ bool ], finalSteinerTree : EdgeWeightedGraphCopy[ T ]) -> T:
		...
