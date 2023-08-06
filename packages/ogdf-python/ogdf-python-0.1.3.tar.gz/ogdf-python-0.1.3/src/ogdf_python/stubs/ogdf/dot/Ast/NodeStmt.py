# file stubs/ogdf/dot/Ast/NodeStmt.py generated from structogdf_1_1dot_1_1_ast_1_1_node_stmt
import enum
from typing import *
from ogdf_python import ogdf, cpp
std = cpp.std
class NodeStmt(ogdf.dot.Ast.Stmt):

	attrs : AttrList = ...

	nodeId : NodeId = ...

	def __init__(self, nodeID : NodeId, attrList : AttrList) -> None:
		...

	def __destruct__(self) -> None:
		...

	def read(self, P : Parser, G : ogdf.Graph, GA : GraphAttributes, C : ClusterGraph, CA : ClusterGraphAttributes, data : SubgraphData) -> bool:
		...
