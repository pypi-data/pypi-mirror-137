# file stubs/ogdf/dot/Ast/Port.py generated from structogdf_1_1dot_1_1_ast_1_1_port
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
class Port(object):

	compassPt : CompassPt = ...

	id : str = ...

	def __init__(self, idString : str, compassPT : CompassPt) -> None:
		...

	def __destruct__(self) -> None:
		...
