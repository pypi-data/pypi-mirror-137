# file stubs/ogdf/dot/Ast/EdgeStmt.py generated from structogdf_1_1dot_1_1_ast_1_1_edge_stmt
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
class EdgeStmt(ogdf.dot.Ast.Stmt):

	attrs : AttrList = ...

	lhs : EdgeLhs = ...

	rhs : EdgeRhs = ...

	def __init__(self, edgeLHS : EdgeLhs, edgeRHS : EdgeRhs, attrList : AttrList) -> None:
		...

	def __destruct__(self) -> None:
		...

	def read(self, P : Parser, G : ogdf.Graph, GA : GraphAttributes, C : ClusterGraph, CA : ClusterGraphAttributes, data : SubgraphData) -> bool:
		...
