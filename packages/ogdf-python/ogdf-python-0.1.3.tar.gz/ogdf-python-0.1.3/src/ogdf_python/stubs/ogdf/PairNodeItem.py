# file stubs/ogdf/PairNodeItem.py generated from structogdf_1_1_pair_node_item
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
class PairNodeItem(object):

	m_it : ListIterator[PairFaceItem] = ...

	m_v : node = ...

	@overload
	def __init__(self) -> None:
		...

	@overload
	def __init__(self, v : node, it : ListIterator[PairFaceItem] = ListIterator[PairFaceItem]()) -> None:
		...
