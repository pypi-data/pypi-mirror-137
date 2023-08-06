# file stubs/ogdf/DecrIndexComparer.py generated from classogdf_1_1_decr_index_comparer
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
POINT = TypeVar('POINT')

class DecrIndexComparer(ogdf.GenericComparer[  int,  int ], Generic[POINT]):

	def __init__(self, box : Array[ POINT ]) -> None:
		...
