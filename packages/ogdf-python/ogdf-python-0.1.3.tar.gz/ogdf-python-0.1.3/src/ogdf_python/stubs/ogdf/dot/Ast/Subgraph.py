# file stubs/ogdf/dot/Ast/Subgraph.py generated from structogdf_1_1dot_1_1_ast_1_1_subgraph
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
class Subgraph(ogdf.dot.Ast.Stmt, ogdf.dot.Ast.EdgeLhs):

	id : str = ...

	statements : StmtList = ...

	def __init__(self, idString : str, statementList : StmtList) -> None:
		...

	def __destruct__(self) -> None:
		...

	def read(self, P : Parser, G : ogdf.Graph, GA : GraphAttributes, C : ClusterGraph, CA : ClusterGraphAttributes, data : SubgraphData) -> bool:
		...
