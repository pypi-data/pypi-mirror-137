# file stubs/ogdf/WeightComparer.py generated from classogdf_1_1_weight_comparer
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
T = TypeVar('T')

class WeightComparer(Generic[T]):

	def __init__(self, pWeight : NodeArray[ T ]) -> None:
		...

	def less(self, v : node, w : node) -> bool:
		...

	def __call__(self, v : node, w : node) -> bool:
		...
