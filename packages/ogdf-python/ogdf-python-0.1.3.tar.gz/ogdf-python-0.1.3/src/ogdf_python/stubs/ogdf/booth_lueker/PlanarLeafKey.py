# file stubs/ogdf/booth_lueker/PlanarLeafKey.py generated from classogdf_1_1booth__lueker_1_1_planar_leaf_key
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
X = TypeVar('X')

class PlanarLeafKey(ogdf.PQLeafKey[ edge, X, bool ], Generic[X]):

	def __init__(self, e : edge) -> None:
		...

	def __destruct__(self) -> None:
		...

	def print(self, os : std.ostream) -> std.ostream:
		"""The functionprint()is a virtual function, that can be overloaded by the user in order to print out the information stored at any of the derived classes."""
		...
