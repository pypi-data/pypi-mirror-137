# file stubs/ogdf/fast_multipole_embedder/FMETreePartition.py generated from structogdf_1_1fast__multipole__embedder_1_1_f_m_e_tree_partition
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
Func = TypeVar('Func')

class FMETreePartition(object):

	"""struct for distributing subtrees to the threads"""

	nodes : std.list[LinearQuadtree.NodeID] = ...

	pointCount : int = ...

	def for_loop(self, func : Func) -> None:
		...
