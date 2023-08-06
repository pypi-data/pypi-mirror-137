# file stubs/ogdf/embedder/ConnectedSubgraph.py generated from classogdf_1_1embedder_1_1_connected_subgraph
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
T = TypeVar('T')

class ConnectedSubgraph(Generic[T]):

	def __init__(self) -> None:
		...

	@overload
	def call(self, G : Graph, SG : Graph, nG : node, nodeLengthG : NodeArray[ T ], nodeLengthSG : NodeArray[ T ]) -> None:
		"""Computes a connected subgraph SG of G containing node nG."""
		...

	@overload
	def call(self, G : Graph, SG : Graph, nG : node, nodeLengthG : NodeArray[ T ], nodeLengthSG : NodeArray[ T ], edgeLengthG : EdgeArray[ T ], edgeLengthSG : EdgeArray[ T ]) -> None:
		"""Computes a connected subgraph SG of G containing node nG."""
		...

	@overload
	def call(self, G : Graph, SG : Graph, nG : node, nodeLengthG : NodeArray[ T ], nodeLengthSG : NodeArray[ T ], nG_to_nSG : NodeArray[node]) -> None:
		"""Computes a connected subgraph SG of G containing node nG."""
		...

	@overload
	def call(self, G : Graph, SG : Graph, nG : node, nSG : node, nodeLengthG : NodeArray[ T ], nodeLengthSG : NodeArray[ T ]) -> None:
		"""Computes a connected subgraph SG of G containing node nG."""
		...

	@overload
	def call(self, G : Graph, SG : Graph, nG : node, nSG : node, nodeLengthG : NodeArray[ T ], nodeLengthSG : NodeArray[ T ], edgeLengthG : EdgeArray[ T ], edgeLengthSG : EdgeArray[ T ]) -> None:
		"""Computes a connected subgraph SG of G containing node nG."""
		...

	@overload
	def call(self, G : Graph, SG : Graph, nG : node, nSG : node, nSG_to_nG : NodeArray[node], eSG_to_eG : EdgeArray[edge], nodeLengthG : NodeArray[ T ], nodeLengthSG : NodeArray[ T ], edgeLengthG : EdgeArray[ T ], edgeLengthSG : EdgeArray[ T ]) -> None:
		"""Computes a connected subgraph SG of G containing node nG."""
		...

	@overload
	def call(self, G : Graph, SG : Graph, nG : node, nSG : node, nSG_to_nG : NodeArray[node], eSG_to_eG : EdgeArray[edge], nG_to_nSG : NodeArray[node], eG_to_eSG : EdgeArray[edge], nodeLengthG : NodeArray[ T ], nodeLengthSG : NodeArray[ T ], edgeLengthG : EdgeArray[ T ], edgeLengthSG : EdgeArray[ T ]) -> None:
		"""Computes a connected subgraph SG of G containing node nG."""
		...

	@overload
	def call(self, G : Graph, SG : Graph, nG : node, nSG_to_nG : NodeArray[node]) -> None:
		"""Computes a connected subgraph SG of G containing node nG."""
		...

	@overload
	def call(self, G : Graph, SG : Graph, nG : node, nSG_to_nG : NodeArray[node], eSG_to_eG : EdgeArray[edge], nG_to_nSG : NodeArray[node], eG_to_eSG : EdgeArray[edge]) -> None:
		"""Computes a connected subgraph SG of G containing node nG."""
		...
