# file stubs/ogdf/SpringEmbedderKK.py generated from classogdf_1_1_spring_embedder_k_k
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
class SpringEmbedderKK(ogdf.LayoutModule):

	"""The spring-embedder layout algorithm by Kamada and Kawai."""

	dpair : Type = Tuple2[ float, float ]

	def __init__(self) -> None:
		"""Constructor: Constructs instance of Kamada KawaiLayout."""
		...

	@overload
	def call(self, GA : GraphAttributes) -> None:
		"""Calls the layout algorithm for graph attributesGA. Currently,GA.doubleWeightis NOT used to allow simple distinction of BFS/APSS. Precondition:Graphis connected."""
		...

	@overload
	def call(self, GA : GraphAttributes, eLength : EdgeArray[ float ]) -> None:
		"""Calls the layout algorithm for graph attributesGAusing values in eLength for distance computation. Precondition:Graphis connected."""
		...

	def computeMaxIterations(self, b : bool) -> None:
		"""If set to true, number of iterations is computed depending on G."""
		...

	def maxGlobalIterations(self) -> int:
		...

	def maxLocalIterations(self) -> int:
		"""It is possible to limit the number of iterations to a fixed value Returns the current setting of iterations. These values are only used if m_computeMaxIt is set to true."""
		...

	def setDesLength(self, d : float) -> None:
		"""Sets desirable edge length directly."""
		...

	def setGlobalIterationFactor(self, i : int) -> None:
		...

	def setMaxGlobalIterations(self, i : int) -> None:
		"""Sets the number of global iterations toi."""
		...

	def setMaxLocalIterations(self, i : int) -> None:
		"""Sets the number of local iterations toi."""
		...

	def setStopTolerance(self, s : float) -> None:
		"""Sets the value for the stop tolerance, below which the system is regarded stable (balanced) and the optimization stopped."""
		...

	def setUseLayout(self, b : bool) -> None:
		"""If set to true, the given layout is used for the initial positions."""
		...

	def setZeroLength(self, d : float) -> None:
		"""If set != 0, value zerolength is used to determine the desirable edge length by L = zerolength / max distance_ij. Otherwise, zerolength is determined using the node number and sizes."""
		...

	def useLayout(self) -> bool:
		...

	def zeroLength(self) -> float:
		...

	def adaptLengths(self, G : Graph, GA : GraphAttributes, eLengths : EdgeArray[ float ], adaptedLengths : EdgeArray[ float ]) -> None:
		"""Changes given edge lengths (interpreted as weight factors) according to additional parameters like node size etc."""
		...

	def computeParDer(self, m : node, u : node, GA : GraphAttributes, ss : NodeArray[NodeArray[ float ] ], dist : NodeArray[NodeArray[ float ] ]) -> dpair:
		"""Computes contribution of node u to the first partial derivatives (dE/dx_m, dE/dy_m) (for node m) (eq. 7 and 8 in paper)"""
		...

	def computeParDers(self, v : node, GA : GraphAttributes, ss : NodeArray[NodeArray[ float ] ], dist : NodeArray[NodeArray[ float ] ]) -> dpair:
		"""Compute partial derivative for v."""
		...

	def doCall(self, GA : GraphAttributes, eLength : EdgeArray[ float ], simpleBFS : bool) -> None:
		"""Does the actual call."""
		...

	def finished(self, maxdelta : float) -> bool:
		"""Checks if main loop is finished because local optimum reached."""
		...

	def finishedNode(self, deltav : float) -> bool:
		"""Checks if inner loop (current node) is finished."""
		...

	def initialize(self, GA : GraphAttributes, partialDer : NodeArray[dpair], eLength : EdgeArray[ float ], oLength : NodeArray[NodeArray[ float ] ], sstrength : NodeArray[NodeArray[ float ] ], simpleBFS : bool) -> None:
		"""Does the necessary initialization work for the call functions."""
		...

	def mainStep(self, GA : GraphAttributes, partialDer : NodeArray[dpair], oLength : NodeArray[NodeArray[ float ] ], sstrength : NodeArray[NodeArray[ float ] ]) -> None:
		"""Main computation loop, nodes are moved here."""
		...

	def scale(self, GA : GraphAttributes) -> None:
		"""Does the scaling if no edge lengths are given but node sizes are respected."""
		...

	def shufflePositions(self, GA : GraphAttributes) -> None:
		"""Adapts positions to avoid degeneracy (all nodes on a single point)"""
		...
