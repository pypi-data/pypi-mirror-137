# file stubs/ogdf/DynamicPlanarSPQRTree.py generated from classogdf_1_1_dynamic_planar_s_p_q_r_tree
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
class DynamicPlanarSPQRTree(ogdf.DynamicSPQRTree, ogdf.PlanarSPQRTree):

	"""SPQR-trees of planar graphs."""

	@overload
	def __init__(self, G : Graph, isEmbedded : bool = False) -> None:
		"""Creates an SPQR tree for planar graphGrooted at the first edge ofG."""
		...

	@overload
	def __init__(self, G : Graph, e : edge, isEmbedded : bool = False) -> None:
		"""Creates an SPQR tree for planar graphGrooted at edgee."""
		...
