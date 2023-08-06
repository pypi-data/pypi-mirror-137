# file stubs/ogdf/dot/Ast/AsgnStmt.py generated from structogdf_1_1dot_1_1_ast_1_1_asgn_stmt
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
class AsgnStmt(ogdf.dot.Ast.Stmt):

	lhs : str = ...

	rhs : str = ...

	def __init__(self, lhsString : str, rhsString : str) -> None:
		...

	def __destruct__(self) -> None:
		...

	def read(self, P : Parser, G : ogdf.Graph, GA : GraphAttributes, C : ClusterGraph, CA : ClusterGraphAttributes, data : SubgraphData) -> bool:
		...
