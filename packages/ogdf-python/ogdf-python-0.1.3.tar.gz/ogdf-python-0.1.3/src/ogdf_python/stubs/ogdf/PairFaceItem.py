# file stubs/ogdf/PairFaceItem.py generated from structogdf_1_1_pair_face_item
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
class PairFaceItem(object):

	m_f : face = ...

	m_it : ListIterator[PairNodeItem] = ...

	@overload
	def __init__(self) -> None:
		...

	@overload
	def __init__(self, f : face) -> None:
		...

	@overload
	def __init__(self, f : face, it : ListIterator[PairNodeItem]) -> None:
		...
