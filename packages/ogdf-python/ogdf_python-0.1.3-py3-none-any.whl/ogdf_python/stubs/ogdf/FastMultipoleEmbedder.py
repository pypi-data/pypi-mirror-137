# file stubs/ogdf/FastMultipoleEmbedder.py generated from classogdf_1_1_fast_multipole_embedder
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
class FastMultipoleEmbedder(ogdf.LayoutModule):

	"""The fast multipole embedder approach for force-directed layout."""

	def __init__(self) -> None:
		"""constructor"""
		...

	def __destruct__(self) -> None:
		"""destructor"""
		...

	@overload
	def call(self, G : Graph, nodeXPosition : NodeArray[ float ], nodeYPosition : NodeArray[ float ], edgeLength : EdgeArray[ float ], nodeSize : NodeArray[ float ]) -> None:
		"""Calls the algorithm for graphGwith the given edgelength and returns the layout information innodeXPosition,nodeYPosition."""
		...

	@overload
	def call(self, GA : GraphAttributes) -> None:
		"""Calls the algorithm for graphGAand returns the layout information inGA."""
		...

	@overload
	def call(self, GA : GraphAttributes, edgeLength : EdgeArray[ float ], nodeSize : NodeArray[ float ]) -> None:
		"""Calls the algorithm for graphGAwith the givenedgeLengthand returns the layout information inGA."""
		...

	def setDefaultEdgeLength(self, edgeLength : float) -> None:
		...

	def setDefaultNodeSize(self, nodeSize : float) -> None:
		...

	def setMultipolePrec(self, precision : int) -> None:
		"""sets the number of coefficients for the expansions. default = 4"""
		...

	def setNumberOfThreads(self, numThreads : int) -> None:
		...

	def setNumIterations(self, numIterations : int) -> None:
		"""sets the maximum number of iterations"""
		...

	def setRandomize(self, b : bool) -> None:
		"""if true, layout algorithm will randomize the layout in the beginning"""
		...
