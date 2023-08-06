# file stubs/ogdf/UpwardPlanarityEmbeddedDigraph.py generated from classogdf_1_1_upward_planarity_embedded_digraph
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
class UpwardPlanarityEmbeddedDigraph(object):

	def __init__(self, H : Graph) -> None:
		...

	@overload
	def isUpwardPlanarEmbedded(self) -> bool:
		...

	@overload
	def isUpwardPlanarEmbedded(self, possibleExternalFaces : List[adjEntry]) -> bool:
		...
