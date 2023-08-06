# file stubs/ogdf/SeqItemXY.py generated from structogdf_1_1_seq_item_x_y
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
class SeqItemXY(object):

	m_iterX : XSequence.iterator = ...

	m_iterY : YSequence.iterator = ...

	@overload
	def __init__(self) -> None:
		...

	@overload
	def __init__(self, iterX : XSequence.iterator) -> None:
		...

	@overload
	def __init__(self, iterY : YSequence.iterator) -> None:
		...
