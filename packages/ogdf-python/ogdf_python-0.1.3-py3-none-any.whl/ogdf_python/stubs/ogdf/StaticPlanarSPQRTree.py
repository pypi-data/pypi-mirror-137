# file stubs/ogdf/StaticPlanarSPQRTree.py generated from classogdf_1_1_static_planar_s_p_q_r_tree
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
class StaticPlanarSPQRTree(ogdf.StaticSPQRTree, ogdf.PlanarSPQRTree):

	"""SPQR-trees of planar graphs."""

	@overload
	def __init__(self, G : Graph, isEmbedded : bool = False) -> None:
		"""Creates an SPQR treeTfor planar graphGrooted at the first edge ofG."""
		...

	@overload
	def __init__(self, G : Graph, e : edge, isEmbedded : bool = False) -> None:
		"""Creates an SPQR treeTfor planar graphGrooted at edgee."""
		...
