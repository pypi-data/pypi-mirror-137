# file stubs/ogdf/PQNodeRoot.py generated from classogdf_1_1_p_q_node_root
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
class PQNodeRoot(object):

	"""The classPQNodeRootis used as a base class of the classPQNode."""

	class PQNodeMark(enum.Enum):

		Unmarked = enum.auto()

		Queued = enum.auto()

		Blocked = enum.auto()

		Unblocked = enum.auto()

	class PQNodeStatus(enum.Enum):

		Empty = enum.auto()

		Partial = enum.auto()

		Full = enum.auto()

		Pertinent = enum.auto()

		ToBeDeleted = enum.auto()

		#: Indicator for extra node status defines.
		Indicator = enum.auto()

		#: Nodes removed during the template reduction are marked as as Eliminated. Their memory is not freed. They are kept for parent pointer update.
		Eliminated = enum.auto()

		#: Nodes that need to be removed in order to obtain a maximal pertinent sequence are marked WhaDelete.
		WhaDelete = enum.auto()

		#: The pertinent Root is marked PertRoot during the clean up after a reduction. Technical.
		PertRoot = enum.auto()

	class PQNodeType(enum.Enum):

		PNode = enum.auto()

		QNode = enum.auto()

		Leaf = enum.auto()

		Undefined = enum.auto()

	class SibDirection(enum.Enum):

		NoDir = enum.auto()

		Left = enum.auto()

		Right = enum.auto()

	def __init__(self) -> None:
		...

	def __destruct__(self) -> None:
		...
