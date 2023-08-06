# file stubs/ogdf/dot/Ast/EdgeRhs.py generated from structogdf_1_1dot_1_1_ast_1_1_edge_rhs
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
class EdgeRhs(object):

	head : EdgeLhs = ...

	tail : EdgeRhs = ...

	def __init__(self, headEdgeLHS : EdgeLhs, tailEdgeRHS : EdgeRhs) -> None:
		...

	def __destruct__(self) -> None:
		...
