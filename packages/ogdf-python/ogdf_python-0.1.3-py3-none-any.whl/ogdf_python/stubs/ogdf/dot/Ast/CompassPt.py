# file stubs/ogdf/dot/Ast/CompassPt.py generated from structogdf_1_1dot_1_1_ast_1_1_compass_pt
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
class CompassPt(object):

	class Type(enum.Enum):

		n = enum.auto()

		ne = enum.auto()

		e = enum.auto()

		se = enum.auto()

		s = enum.auto()

		sw = enum.auto()

		w = enum.auto()

		nw = enum.auto()

		c = enum.auto()

		wildcard = enum.auto()

	type : Type = ...

	def __init__(self, paramType : Type) -> None:
		...

	def __destruct__(self) -> None:
		...
