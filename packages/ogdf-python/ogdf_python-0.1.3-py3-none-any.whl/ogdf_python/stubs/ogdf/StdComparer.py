# file stubs/ogdf/StdComparer.py generated from classogdf_1_1_std_comparer_3_01_prioritized_3_01_x_00_01_priority_01_4_01_4
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
Priority = TypeVar('Priority')

X = TypeVar('X')

class StdComparer(Generic[X, Priority]):

	def equal(self, x : Prioritized[ X, Priority ], y : Prioritized[ X, Priority ]) -> bool:
		...

	def geq(self, x : Prioritized[ X, Priority ], y : Prioritized[ X, Priority ]) -> bool:
		...

	def greater(self, x : Prioritized[ X, Priority ], y : Prioritized[ X, Priority ]) -> bool:
		...

	def leq(self, x : Prioritized[ X, Priority ], y : Prioritized[ X, Priority ]) -> bool:
		...

	def less(self, x : Prioritized[ X, Priority ], y : Prioritized[ X, Priority ]) -> bool:
		...
