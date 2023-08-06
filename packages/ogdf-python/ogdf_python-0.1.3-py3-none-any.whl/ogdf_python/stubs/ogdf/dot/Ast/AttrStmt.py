# file stubs/ogdf/dot/Ast/AttrStmt.py generated from structogdf_1_1dot_1_1_ast_1_1_attr_stmt
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
class AttrStmt(ogdf.dot.Ast.Stmt):

	class Type(enum.Enum):

		graph = enum.auto()

		edge = enum.auto()

		node = enum.auto()

	attrs : AttrList = ...

	type : Type = ...

	def __init__(self, paramType : Type, attrList : AttrList) -> None:
		...

	def __destruct__(self) -> None:
		...

	def read(self, P : Parser, G : ogdf.Graph, GA : GraphAttributes, C : ClusterGraph, CA : ClusterGraphAttributes, data : SubgraphData) -> bool:
		...
