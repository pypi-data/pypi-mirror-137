# file stubs/ogdf/embedder/LayersBlockEmbedder.py generated from classogdf_1_1embedder_1_1_layers_block_embedder
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
BaseEmbedder = TypeVar('BaseEmbedder')

T = TypeVar('T')

class LayersBlockEmbedder(BaseEmbedder, Generic[BaseEmbedder, T]):

	"""Common functionality for layer-based embedding algorithms."""

	def internalEmbedBlock(self, SG : Graph, nodeLengthSG : NodeArray[ T ], edgeLengthSG : EdgeArray[ T ], nSG_to_nG : NodeArray[node], eSG_to_eG : EdgeArray[edge], nodeInBlockSG : node, cT : node, after : ListIterator[adjEntry]) -> None:
		...
