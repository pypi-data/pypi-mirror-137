# file stubs/ogdf/dot/Ast/Stmt.py generated from structogdf_1_1dot_1_1_ast_1_1_stmt
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
class Stmt(object):

	def __destruct__(self) -> None:
		...

	def read(self, P : Parser, G : ogdf.Graph, GA : GraphAttributes, C : ClusterGraph, CA : ClusterGraphAttributes, data : SubgraphData) -> bool:
		...
