# file stubs/ogdf/SeqItemY.py generated from structogdf_1_1_seq_item_y
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
class SeqItemY(object):

	m_iterY : YSequence.iterator = ...

	m_origNode : node = ...

	@overload
	def __init__(self) -> None:
		...

	@overload
	def __init__(self, vOrig : node) -> None:
		...

	@overload
	def __init__(self, iterY : YSequence.iterator) -> None:
		...
