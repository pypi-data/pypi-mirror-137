# file stubs/ogdf/GlueMap.py generated from classogdf_1_1_glue_map
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
Cost = TypeVar('Cost')

class GlueMap(Generic[Cost]):

	"""This is a helper class to make the glueing of two edges simpler."""

	#: The core edge that will be deleted.
	m_eLoser : edge = ...

	#: The core edge that will survive.
	m_eWinner : edge = ...

	#: The graph that eLoser represents.
	m_gLoser : Graph = ...

	#: The graph that eWinner represents.
	m_gWinner : Graph = ...

	#: A map from the edges of the loser graph to their new home in the winner graph.
	m_mapE_l2w : EdgeArray[edge] = ...

	#: A map from the edges of the loser graph to the original graph, to denote the original of each node.
	m_mapEloser : EdgeArray[edge] = ...

	#: A map from the edges of the winner graph to the original graph, to denote the original of each edge.
	m_mapEwinner : EdgeArray[edge] = ...

	#: A map from the nodes of the loser graph to their new home in the winner graph.
	m_mapV_l2w : NodeArray[node] = ...

	#: A map from the nodes of the loser graph to the original graph, to denote the original of each node.
	m_mapVloser : NodeArray[node] = ...

	#: A map from the nodes of the winner graph to the original graph, to denote the original of each edge.
	m_mapVwinner : NodeArray[node] = ...

	#: TheNonPlanarCoreon which this instance operates.
	m_npc : NonPlanarCore[ Cost ] = ...

	def __init__(self, eWinner : edge, eLoser : edge, npc : NonPlanarCore[ Cost ]) -> None:
		"""AGlueMapis created from anNonPlanarCoreand two core edges that ought to be glued together."""
		...

	def getLoserGraph(self) -> Graph:
		"""Getter form_gLoser."""
		...

	def getWinnerNodeOfLoserNode(self, v : node) -> node:
		"""Getter form_mapV_l2w."""
		...

	def mapLoserToNewWinnerEdge(self, eInLoser : edge) -> None:
		"""A mapping from theeInLosergraph to a new edge in the winner graph is created."""
		...

	def mapLoserToNewWinnerNode(self, vInLoser : node) -> None:
		"""A mapping from thevInLoserto a new node in the winner graph is created."""
		...

	def mapLoserToWinnerNode(self, vInLoser : node, vInWinner : node) -> None:
		"""A mapping from thevInLoserto thevInWinneris created."""
		...

	def reorder(self, vLoser : node, sameDirection : bool, isTNodeOfPNode : bool) -> None:
		"""This method reorders the adjacency order ofvLoser'scounterpart in the winner graph according to the AdjOrder ofvLoserin the loser graph."""
		...
